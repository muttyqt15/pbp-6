from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UsernameForm, CustomerProfileForm, OwnerProfileForm
from .models import CustomerProfile, OwnerProfile

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
