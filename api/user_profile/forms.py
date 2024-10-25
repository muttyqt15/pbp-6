from django import forms
from django.contrib.auth import get_user_model
from .models import CustomerProfile, OwnerProfile

User = get_user_model()

class UsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['bio']

class OwnerProfileForm(forms.ModelForm):
    class Meta:
        model = OwnerProfile
        fields = ['bio']
