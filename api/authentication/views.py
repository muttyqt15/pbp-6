from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import SignupForm, LoginForm


# Signup view
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "authentication:login"
            )  # Redirect to login after successful signup
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
                return redirect(
                    "main:index"
                )  # Redirect to home after login OR authenticated page
            else:
                # Invalid credentials
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


# Logout view
def logout(request):
    auth_logout(request)
    return redirect("authentication:login")  # Redirect to login page after logout


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# Signup view
@csrf_exempt
def signup_flutter(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            form = SignupForm(data)
            if form.is_valid():
                form.save()
                auth_login(request, user)
                return JsonResponse(
                    {"success": True, "message": "Signup successful. Please log in."},
                    status=201,
                )
            else:
                return JsonResponse(
                    {"success": False, "errors": form.errors}, status=400
                )
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "message": "Invalid JSON data"}, status=400
            )
    return JsonResponse(
        {"success": False, "message": "Only POST requests are allowed"}, status=405
    )


# Login view
@csrf_exempt
def login_flutter(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            form = LoginForm(data)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    return JsonResponse(
                        {"success": True, "message": "Login successful"}, status=200
                    )
                else:
                    return JsonResponse(
                        {"success": False, "message": "Invalid username or password"},
                        status=401,
                    )
            else:
                return JsonResponse(
                    {"success": False, "errors": form.errors}, status=400
                )
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "message": "Invalid JSON data"}, status=400
            )
    return JsonResponse(
        {"success": False, "message": "Only POST requests are allowed"}, status=405
    )


# Logout view
@csrf_exempt
def logout_flutter(request):
    if request.method == "POST":
        auth_logout(request)
        return JsonResponse(
            {"success": True, "message": "Logout successful"}, status=200
        )
    return JsonResponse(
        {"success": False, "message": "Only POST requests are allowed"}, status=405
    )
