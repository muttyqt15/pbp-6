from django import forms
from .models import CustomerProfile, OwnerProfile


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['bio']

class OwnerProfileForm(forms.ModelForm):
    class Meta:
        model = OwnerProfile
        fields = ['bio']

class CustomerProfilePictureForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile  # Use OwnerProfile for restaurant owners
        fields = ['profile_pic_url']

class OwnerProfilePictureForm(forms.ModelForm):
    class Meta:
        model = OwnerProfile  # Use OwnerProfile for restaurant owners
        fields = ['profile_pic_url']

