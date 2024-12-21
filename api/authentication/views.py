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
from .models import User


@csrf_exempt
def signup_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']
        role = data['role']

        # Check if the passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)
        
        # Create the new user
        user = User.objects.create_user(username=username, password=password1)
        user.role = role
        user.save()
        
        return JsonResponse({
            "username": user.username,
            "status": 'success',
            "message": "User created successfully!"
        }, status=200)
    
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)
# Login view
@csrf_exempt
def login_flutter(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    user_data = {
                        "id": request.user.id,
                        "username": request.user.username,
                        "email": request.user.email,
                        "role": request.user.role
                    }
                    return JsonResponse(
                        {
                            "success": True,
                            "message": "Login successful",
                            "data": user_data,
                        },
                        status=200,
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
            print(request.body)
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