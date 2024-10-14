from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            return redirect("/admin")


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            form.save()  # This saves the user and the uploaded file
            return redirect("/admin/")
    else:
        form = SignUpForm()
    return render(request, "login.html", {"form": form})
