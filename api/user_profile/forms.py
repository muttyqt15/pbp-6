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

class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['username']  # Include the fields you want to edit

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Set initial values for bio if it exists
            if hasattr(user, 'customerprofile'):
                self.fields['bio'].initial = user.customerprofile.bio
            elif hasattr(user, 'ownerprofile'):
                self.fields['bio'].initial = user.ownerprofile.bio