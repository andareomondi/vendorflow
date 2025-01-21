from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *

# Create your views here.
class Home(LoginRequiredMixin, View):
  def get(self, request):
    machines = Machine.objects.all()
    transactions = Transaction.objects.order_by('-date')
    total_sales = sum(machine.total_amount for machine in machines)
    total_transactions = sum(transaction.amount for transaction in Transaction.objects.all())
    context = {
        'machines': machines,
        'transactions': transactions,
        'total_sales': total_sales,
        'total_transactions': total_transactions,
    }
    return render(request, 'vending/home.html', context = context)

  def post(self, request):
    name = request.POST.get('name')
    location = request.POST.get('location')
    serial_number = request.POST.get('serial_number')
    machine_typer = request.POST.get('machine_typer')
    user = request.user
    # machine = Machine.objects.get(serial_number = serial_number)
    if Machine.objects.filter(serial_number=serial_number).exists():
      messages.error(request, 'Machinen already in the system')
      return redirect('home')
    else:
      machine = Machine(name=name, location=location, serial_number=serial_number, machine_type=machine_typer, owner=user)
      machine.save()
      messages.success(request, 'New machine registered')
      return redirect('home')


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
    pass


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
        return redirect('home')

    return render(request, 'vending/register.html', {'form': form})

def logout_user(request):
  if request.method == 'POST':
    logout(request)
    return redirect('login')


class About(View):
  def get(self, request):
    return render(request, 'vending/about.html')
