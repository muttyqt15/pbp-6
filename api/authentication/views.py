from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import SignupForm, LoginForm


# Signup view
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("auth:login")  # Redirect to login after successful signup
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})


# Login view
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("main:main")  # Redirect to home after login
            else:
                # Invalid credentials
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


# Logout view
def logout(request):
    auth_logout(request)
    return redirect("login")  # Redirect to login page after logout
