from django.shortcuts import render
from .forms import LoginForm, SignUpForm


# Create your views here.
def login(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, "login.html", {"form": form})
