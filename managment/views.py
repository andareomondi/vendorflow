from django.shortcuts import render, redirect
from django.views import View
from vending.models import *
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from vending.forms import MachineForm
# Create your views here.
class Dashboard(LoginRequiredMixin, View):
  def get(self, request):
    if request.user.is_superuser:
      form = MachineForm()
      machines = Machine.objects.order_by('id')
      refills = Refill.objects.filter(status='Pending', payment_made=True)
      context = {
        'machines': machines,
        'refills': refills,
        'form': form,
      }
      return render(request, 'managment/dashboard.html', context)
    else:
      messages.error(request, 'You are not authorized to view the admin dashboard')
      return redirect('home')
  def post(self, request):
    refill_id = request.POST.get('button')
    refill = Refill.objects.get(id=refill_id)
    refill.status = 'Approved'
    refill.save()
    refill.refill_tokens()
    messages.success(request, 'Refill Approved')
    return redirect('dashboard')