from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, RestaurantOwner, Customer
from .constant import Role

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "role"]

    role = forms.ChoiceField(choices=Role.get_roles(), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set placeholders and labels for the fields
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email address'
        self.fields['password1'].widget.attrs['placeholder'] = 'Create a password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'
        
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['role'].label = 'Role'

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already in use.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data["role"]

        if commit:
            user.save()  # First save the user to associate foreign keys later.
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
