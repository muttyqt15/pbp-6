from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from .forms import UsernameForm, CustomerProfileForm, OwnerProfileForm, UserProfileForm
from .models import CustomerProfile, OwnerProfile
from api.authentication.models import User, RestaurantOwner, Customer
from api.review.models import Review
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views.decorators.csrf import csrf_exempt


@receiver(post_save, sender=User )
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_resto_owner:
            RestaurantOwner.objects.create(user=instance)
        else:
            Customer.objects.create(user=instance)


@login_required
def profile_view(request):
    user = request.user
    customer_profile = None
    owner_profile = None

    if user.is_customer:
        customer_profile = CustomerProfile.objects.get(user=user)
    elif user.is_resto_owner:
        owner_profile = OwnerProfile.objects.get(user=user)

    return render(request, 'my_profile.html', {
        'customer_profile': customer_profile,
        'owner_profile': owner_profile,
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'updated_username': request.user.username,
                'updated_bio': request.user.profile.bio,  # Assuming you have a profile model
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


@login_required
@csrf_exempt  
def edit_owner_profile(request):
    user_form = UsernameForm(instance=request.user)
    profile_form = OwnerProfileForm(instance=request.user.ownerprofile)
    
    if request.method == 'POST':
        user_form = UsernameForm(request.POST, instance=request.user)
        profile_form = OwnerProfileForm(request.POST, request.FILES, instance=request.user.ownerprofile)  
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return JsonResponse({'success': True, 'redirect_url': '/my-profile/'})  

        return JsonResponse({'success': False, 'errors': user_form.errors | profile_form.errors})

    return JsonResponse({'success': False, 'errors': 'Invalid request method.'})

def logout_user(request):
    logout(request)
    return redirect('main:login')

def delete_account(request):
    if request.method == 'POST':
        user = request.user
        
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
        
        user.delete()
        
        messages.success(request, "Your account has been successfully deleted.")
        return redirect('login') 
    
    return HttpResponseForbidden("Invalid request method.")

# @login_required
# def bookmarks_view(request):
#     user = request.user
#     customer_profile = CustomerProfile.objects.get(user=user)
#     bookmarks = customer_profile.bookmarks.all()  # Assuming bookmarks is a ManyToManyField

#     return render(request, 'bookmarks.html', {
#         'bookmarks': bookmarks,
#     })

@login_required
def review_history_view(request):
    return redirect('/review/""')
    user = request.user
    reviews = Review.objects.filter(user=user) 

    return render(request, 'all_review.html', {
        'reviews': reviews,
    })


@login_required
def my_restaurant_view(request):
    return redirect('/restaurant/""')
    user = request.user
    # Get the restaurant owner profile
    owner_profile = get_object_or_404(OwnerProfile, user=user)
    
    # Get the associated restaurant
    restaurant = owner_profile.restaurant
    
    return render(request, 'restaurant.html', {
        'restaurant': restaurant,
    })

@login_required
def other_profile_view(request, username):
    user = get_object_or_404(User, username=username)

    customer_profile = None
    owner_profile = None

    if user.is_customer:
        customer_profile = get_object_or_404(CustomerProfile, user=user)
    elif user.is_resto_owner:
        owner_profile = get_object_or_404(OwnerProfile, user=user)

    return render(request, 'other_profile.html', {
        'user': user,
        'customer_profile': customer_profile,
        'owner_profile': owner_profile,
    })