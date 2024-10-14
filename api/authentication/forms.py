from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .constant import Role


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True, help_text="Required.")
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        help_text="Required. Enter your password.",
        label="Password",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        help_text="Required. Confirm your password.",
        label="Confirm Password",
    )
    profile_image = forms.ImageField(
        required=False, help_text="Optional. Upload your profile image."
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text="Required. Enter a valid email address.",
    )
    role = forms.ChoiceField(
        choices=Role.get_roles(),
        required=True,
        help_text="Select your role.",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "profile_image",
            "role",
        )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254, required=True, help_text="Required. Enter your username."
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        help_text="Required. Enter your password.",
    )
