from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from .forms import UsernameForm, CustomerProfileForm, OwnerProfileForm
from .models import CustomerProfile, OwnerProfile

@login_required
def profile_view(request):
    user = request.user
    customer_profile = None
    owner_profile = None

    # Check if the user is a customer or owner
    if user.is_customer:
        customer_profile = CustomerProfile.objects.get(user=user)
    elif user.is_resto_owner:
        owner_profile = OwnerProfile.objects.get(user=user)

    return render(request, 'profile.html', {
        'customer_profile': customer_profile,
        'owner_profile': owner_profile,
    })

@login_required
@csrf_exempt  # You may want to handle CSRF tokens properly in a production environment
def edit_customer_profile(request):
    user_form = UsernameForm(instance=request.user)
    profile_form = CustomerProfileForm(instance=request.user.customerprofile)
    
    if request.method == 'POST':
        user_form = UsernameForm(request.POST, instance=request.user)
        profile_form = CustomerProfileForm(request.POST, instance=request.user.customerprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return JsonResponse({'success': True, 'redirect_url': '/profile_view/'})  # Adjust the URL as needed

        return JsonResponse({'success': False, 'errors': user_form.errors | profile_form.errors})

    return JsonResponse({'success': False, 'errors': 'Invalid request method.'})

@login_required
def edit_owner_profile(request):
    user_form = UsernameForm(instance=request.user)
    profile_form = OwnerProfileForm(instance=request.user.ownerprofile)
    
    if request.method == 'POST':
        user_form = UsernameForm(request.POST, instance=request.user)
        profile_form = OwnerProfileForm(request.POST, instance=request.user.ownerprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile_view')  # Redirect to the profile viewing page

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def logout_user(request):
    logout(request)
    return redirect('main:login')

def delete_account(request):
    if request.method == 'POST':
        user = request.user
        
        # Check if the user has a CustomerProfile or OwnerProfile
        try:
            customer_profile = CustomerProfile.objects.get(user=user)
            customer_profile.delete()
        except CustomerProfile.DoesNotExist:
            pass
        
        try:
            owner_profile = OwnerProfile.objects.get(user=user)
            owner_profile.delete()
        except OwnerProfile.DoesNotExist:
            pass
        
        # Delete the user account
        user.delete()
        
        messages.success(request, "Your account has been successfully deleted.")
        return redirect('home')  # Redirect to a home page or another appropriate page
    
    return HttpResponseForbidden("Invalid request method.")
