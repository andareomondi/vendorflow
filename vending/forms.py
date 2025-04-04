from .models import *

from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name' ,'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ['serial_number', 'machine_type']

class MachineActivationForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ['name', 'machine_type' , 'location']

class MachineUpdateForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ['name', 'machine_type' , 'location']

class ShopsForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'location']