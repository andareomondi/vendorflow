from django.shortcuts import render, redirect
from django.views import View
from vending.models import *
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class Dashboard(LoginRequiredMixin, View):
  def get(self, request):
    if request.user.is_superuser:

      machines = Machine.objects.all()
      refills = Refill.objects.filter(status='Pending')
      context = {
        'machines': machines,
        'refills': refills,
      }
      return render(request, 'managment/dashboard.html', context)
    else:
      messages.error(request, 'You are not authorized to view the admin dashboard')
      return redirect('home')