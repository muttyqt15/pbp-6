from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UsernameForm, CustomerProfileForm, OwnerProfileForm
from .models import CustomerProfile, OwnerProfile

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.models import Customer, RestaurantOwner
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
def edit_customer_profile(request):
    user_form = UsernameForm(instance=request.user)
    profile_form = CustomerProfileForm(instance=request.user.customerprofile)
    
    if request.method == 'POST':
        user_form = UsernameForm(request.POST, instance=request.user)
        profile_form = CustomerProfileForm(request.POST, instance=request.user.customerprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile_view')  # Redirect to the profile viewing page

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

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
