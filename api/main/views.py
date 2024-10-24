from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    user = request.user
    ctx = {"user": user}
    return render(request, "main.html", ctx)


@login_required()
def authenticated_page(request):
    user = request.user
    print(request.user)
    ctx = {"user": user}
    return render(request, "authenticated_page.html", ctx)
