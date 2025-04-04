from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, MachineActivationForm, ShopsForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import render_to_string, get_template
from django.http import HttpResponse
from django.core.mail import send_mail
from django.db.models import Count


# Create your views here.
class Home(LoginRequiredMixin, View):
  def get(self, request):
    user = request.user
    send_mail(
        "this is a test",
        "here is the message",
        "shadrackandare@gmail.com",
        ["andareomondi@gmail.com"],
        fail_silently=False,
        )
    shops = Shop.objects.filter(owner=user)
    total_sales = sum(shop.amount for shop in shops)
    customers = sum(shop.customers_served for shop in shops)
    amount = sum(shop.amount for shop in shops)
    form = ShopsForm()
    context = {
      'shops': shops,
      'customers': customers,
      'total_sales': total_sales,
      'amount': amount,
      'form': form,
    }
    return render(request, 'vending/home.html', context = context)

  def post(self, request):
    form = ShopsForm(request.POST)
    if form.is_valid():
      shop = form.save(commit=False)
      shop.owner = request.user
      shop.save()
      messages.success(request, 'Shop created successfully')
      return redirect('home')
    return render(request, 'vending/home.html', {'form': form})


class Specific_Machine(LoginRequiredMixin, View):
  def get(self, request, pk):
    machine = Machine.objects.get(id=pk)
    transactions = Transaction.objects.filter(machine=machine).order_by('-date')
    refills = Refill.objects.filter(machine=machine).order_by('-date')
    context = {
      'machine': machine,
      'transactions': transactions,
      'refills': refills,
    }
    return render(request, 'vending/machine_detail.html', context=context)
  def post(self, request, pk):
    machine = Machine.objects.get(id=pk)
    package = request.POST.get('packageName')
    payment_made = request.POST.get('paymentMade')
    if payment_made == 'yes':
      payment_made = True
    else:
      payment_made = False

    refill = Refill(machine=machine, token_pack=package, status='Pending', payment_made=payment_made)
    refill.save()
    messages.success(request, 'Refill request submitted successfully. Please wait for approval')
    return redirect('specific_machine', pk=pk)


class Register(View):
  def get(self, request):
    if not request.user.is_authenticated:
      form = UserRegistrationForm()
      return render(request, 'vending/register.html', {'form': form})
    else:
      return redirect('home')
  def post(self, request):
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.set_password(form.cleaned_data['password'])
      user.save()
      user = authenticate(username=user.username, password=form.cleaned_data['password'])
      if user is not None:
        login(request, user)
        messages.success(request, 'User creation was succesfull')
        return redirect('home')

    return render(request, 'vending/register.html', {'form': form})

class LogOut(View):
  def post(self, request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')


class About(View):
  def get(self, request):
    return render(request, 'vending/about.html')

# pdf generation for machine's overview
def user_overview_pdf(request):
    owner = request.user
    machines = Machine.objects.filter(owner=owner)
    user = User.objects.get(username=owner)
    transactions = Transaction.objects.select_related('machine__owner').all()
    total_transactions = sum(transaction.amount for transaction in Transaction.objects.all())
    total_sales = sum(machine.total_amount for machine in machines)
    template = get_template('vending/owner_overview_pdf.html')
    context = {
        'owner': user,
        'machines': machines,
        'transactions': transactions,
        'total_transactions': total_transactions,
        'total_sales': total_sales,
        'generation_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    html = template.render(context)

    # Create a PDF
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Error Rendering PDF', status=400)

def machine_overview_pdf(request, pk):
  machine = Machine.objects.get(id=pk)
  transactions = Transaction.objects.filter(machine=machine).order_by('-date')
  refills = Refill.objects.filter(machine=machine).order_by('-date')
  template = get_template('vending/machine_overview_pdf.html')
  context = {
    'machine': machine,
    'transactions': transactions,
    'refills': refills,
    'generation_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
  html = template.render(context)

  # Create a PDF
  result = BytesIO()
  pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

  if not pdf.err:
    return HttpResponse(result.getvalue(), content_type='application/pdf')
  return HttpResponse('Error Rendering PDF', status=400)

class MachineRegistration(View):
  def get(self, request, *arg, **kwargs):
    query = request.GET.get('q')
    try:
      machine = Machine.objects.get(serial_number=query)
    except Machine.DoesNotExist:
      machine = None
    if machine:
      return redirect(to='machine_activation', id=machine.id)
    else:
      messages.error(request, 'Machine not found')
      return redirect('home')

    # return render(reqeust, 'vending/machine_registration.html')

  def post(self, request):
    serial_number = request.POST.get('serial_number')
    machine_type = request.POST.get('machine_type')
    user = request.user
    location = None
    name = None
    shop = None
    if Machine.objects.filter(serial_number=serial_number).exists():
      messages.error(request, 'Machine already in the system')
      return redirect('dashboard')
    else:
      machine = Machine(name=name, location=location, serial_number=serial_number, machine_type=machine_type, owner=user)
      machine.save()
      messages.success(request, 'Machine registered successfully')
      return redirect('dashboard')


class MachineActivation(LoginRequiredMixin, View):
  def get(self, request, id, *args, **kwargs):
    machine = Machine.objects.get(id=id)
    form = MachineActivationForm(instance=machine)
    context = {
      'form': form,
    }
    return render(request, 'vending/machine_activation.html', context=context)
  def post(self, request, id, *args, **kwargs):
    machine = Machine.objects.get(id=id)
    form = MachineActivationForm(request.POST, instance=machine)
    if form.is_valid():
      machine = form.save(commit=False)
      machine.owner = request.user
      machine.activated = True
      machine.save()
      messages.success(request, 'Machine activated successfully')
      return redirect('home')
    return render(request, 'vending/machine_activation.html', context={'form': form})

def deleteMachine(request, pk):
  machine = Machine.objects.get(id=pk)
  transactions = Transaction.objects.filter(machine=machine).order_by('-date')
  refills = Refill.objects.filter(machine=machine).order_by('-date')
  template = get_template('vending/machine_overview_pdf.html')
  context = {
    'machine': machine,
    'transactions': transactions,
    'refills': refills,
    'generation_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
  html = template.render(context)

  # Create a PDF
  result = BytesIO()
  pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

  if not pdf.err:
    messages.success(request, 'Machine deleted succesfully')
    machine.delete()
    return HttpResponse(result.getvalue(), content_type='application/pdf')
  return HttpResponse('Error Rendering PDF', status=400)

class MachineUpdate(LoginRequiredMixin, View):
  def get(self, request, pk):
    machine = Machine.objects.get(id=pk)
    form = MachineActivationForm(instance=machine)
    context = {
      'form': form,
    }
    return render(request, 'vending/machine_update.html', context=context)
  def post(self, request, pk):
    machine = Machine.objects.get(id=pk)
    form = MachineActivationForm(request.POST, instance=machine)
    if form.is_valid():
      form.save()
      messages.success(request, 'Machine updated successfully')
      return redirect('home')
    return render(request, 'vending/machine_update.html', context={'form': form})

def deleteRefill(request, pk):
  refill = Refill.objects.get(id=pk)
  refill.delete()
  messages.success(request, 'Refill request deleted succesfully')
  return redirect('home')

class Shops(View):
  def get(self, request):
    user = request.user
    shops = Shop.objects.filter(owner=user).annotate(machine_count=Count('related_shop'))
    # if no shops redirect to home and display message
    if not shops:
      messages.error(request, 'No shops found')
      return redirect('home')
    context = {
      'shops': shops,
    }
    return render(request, 'vending/shops.html', context=context)

class SpecificShop(LoginRequiredMixin, View):
    def get(self, request, pk):
        shop = Shop.objects.get(id=pk)
        machines = Machine.objects.filter(shop=shop)
        transactions = Transaction.objects.filter(machine__in=machines).order_by('-date')
        total_sales = sum(machine.total_amount for machine in machines)
        context = {
            'shop': shop,
            'machines': machines,
            'transactions': transactions,
            'total_sales': total_sales,
        }
        return render(request, 'vending/shop_detail.html', context=context)