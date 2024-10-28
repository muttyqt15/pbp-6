from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from .forms import CustomerProfileForm, OwnerProfileForm
from .models import CustomerProfile, OwnerProfile
from api.authentication.models import User, RestaurantOwner, Customer
from api.review.models import Review
from django.db.models.signals import post_save
from django.views.decorators.csrf import csrf_exempt
from django.dispatch import receiver


# @receiver(post_save, sender=User )
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.is_resto_owner:
#             RestaurantOwner.objects.create(user=instance)
#         else:
#             Customer.objects.create(user=instance)

@login_required
def profile_view(request):
    user = request.user
    print(user.is_resto_owner)
    try:
        if user.is_resto_owner:
            user_resto = RestaurantOwner.objects.get(user=user)
            userNow = OwnerProfile.objects.get(user=user_resto)
        else:
            user_customer = Customer.objects.get(user=user)
            userNow = CustomerProfile.objects.get(user=user_customer)

        # userNow = OwnerProfile.objects.all()
        # user_resto = RestaurantOwner.objects.get(user=user)

        # print(user_resto)
        # for userr in userNow:
        #     print(userr.user)
        
        return render(request, 'my_profile.html', {
            'userNow': userNow, 'user': user
        })
    
    except OwnerProfile.DoesNotExist:
        # Jika OwnerProfile tidak ada, arahkan ke form untuk membuat profil atau halaman error
        messages.error(request, "Profil pemilik belum tersedia. Silakan buat profil.")
        return redirect('create_owner_profile')
    
    except CustomerProfile.DoesNotExist:
        # Jika CustomerProfile tidak ada, arahkan ke form untuk membuat profil atau halaman error
        messages.error(request, "Profil pelanggan belum tersedia. Silakan buat profil.")
        return redirect('create_customer_profile')

    except RestaurantOwner.DoesNotExist:
        messages.error(request, "Pengguna tidak memiliki restoran yang terkait.")
        return redirect('main:login')

    except Customer.DoesNotExist:
        messages.error(request, "Pengguna tidak memiliki profil pelanggan yang terkait.")
        return redirect('main:login')
    

@login_required
def delete_account(request):
    if request.method == 'GET':
        user = request.user
        
        try:
            # Hapus CustomerProfile jika ada
            customer = Customer.objects.filter(user=user).first()
            if customer:
                customer_profile = CustomerProfile.objects.filter(user=customer).first()
                if customer_profile:
                    customer_profile.delete()
                customer.delete()

            # Hapus OwnerProfile jika ada
            restaurant_owner = RestaurantOwner.objects.filter(user=user).first()
            if restaurant_owner:
                owner_profile = OwnerProfile.objects.filter(user=restaurant_owner).first()
                if owner_profile:
                    owner_profile.delete()
                restaurant_owner.delete()

            # Hapus user
            user.delete()

            # Set pesan sukses dan redirect ke halaman login
            messages.success(request, "Your account has been successfully deleted.")
            return HttpResponseRedirect(reverse('main:login'))
        
        except Exception as e:
            messages.error(request, "There was an error deleting your account.")
            return HttpResponseRedirect(reverse('profile:profile'))

    return HttpResponseForbidden("Invalid request method.")

# @login_required
# def delete_account(request):
#     if request.method == 'GET':
#         user = request.user
        
#         try:
#             # Hapus CustomerProfile jika ada
#             customer_profile = CustomerProfile.objects.filter(user=user).first()
#             print(customer_profile)
#             if customer_profile:
#                 customer_profile.delete()

#             # Hapus OwnerProfile jika ada
#             owner_profile = OwnerProfile.objects.filter(user=user).first()
#             print(owner_profile)
#             if owner_profile:
#                 owner_profile.delete()

#             # Hapus user
#             print(user)
#             user.delete()

#             # Set pesan sukses dan redirect ke halaman login
#             messages.success(request, "Your account has been successfully deleted.")
#             return redirect('news:show_main')
        
#         except Exception as e:
#             messages.error(request, "There was an error deleting your account.")
#             return redirect('profile:profile')

#     return HttpResponseForbidden("Invalid request method.")

# @login_required
# def edit_profile(request):
#     if request.method == 'POST':
#         # Check user role and fetch the corresponding form
#         if request.user.is_resto_owner:
#             user_resto = RestaurantOwner.objects.get(user=request.user)
#             old_form = OwnerProfile.objects.get(user=user_resto)
#             form = OwnerProfileForm(request.POST, request.FILES, instance=old_form)
#             if form.is_valid():
#                 form.save()
#                 return JsonResponse({
#                     'success': True,
#                     'updated_username': request.user.username,
#                     'updated_email': request.user.email,  # updated email
#                     'updated_bio': request.user.bio,
#                 })
#             else:
#                 return JsonResponse({'success': False, 'errors': form.errors})

#         else:
#             user_customer = Customer.objects.get(user=request.user)
#             old_form = CustomerProfile.objects.get(user=user_customer)
#             form = CustomerProfileForm(request.POST, request.FILES, instance=old_form)
#             if form.is_valid():
#                 form.save()
#                 return JsonResponse({
#                     'success': True,
#                     'updated_username': request.user.username,
#                     'updated_email': request.user.email,  # updated email
#                     'updated_bio': request.user.bio,
#                 })
#             return JsonResponse({'success': False, 'errors': form.errors})

#     # Load initial data to populate the modal fields
#     initial_data = {
#         'username': request.user.username,
#         'email': request.user.email,
#         'bio': request.user.bio,
#     }

#     return render(request, 'edit_profile.html', {'initial_data': initial_data})
@login_required
def edit_profile(request):
    if request.method == 'POST':
        if request.user.is_resto_owner:
            # Jika pengguna adalah RestaurantOwner
            user_resto = RestaurantOwner.objects.get(user=request.user)
            old_form = OwnerProfile.objects.get(user=user_resto)
            form = OwnerProfileForm(request.POST, request.FILES, instance=old_form)
            
            if form.is_valid():
                form.save()
                return JsonResponse({
                    'success': True,
                    'updated_username': request.user.username,
                    'updated_email': request.user.email,
                    'updated_bio': old_form.bio,  # Mengakses bio dari OwnerProfile
                })
            else:
                return JsonResponse({'success': False, 'errors': form.errors})

        elif request.user.is_customer:
            # Jika pengguna adalah Customer
            user_customer = Customer.objects.get(user=request.user)
            old_form = CustomerProfile.objects.get(user=user_customer)
            form = CustomerProfileForm(request.POST, request.FILES, instance=old_form)
            
            if form.is_valid():
                form.save()
                return JsonResponse({
                    'success': True,
                    'updated_username': request.user.username,
                    'updated_email': request.user.email,
                    'updated_bio': old_form.bio,  # Mengakses bio dari CustomerProfile
                })
            return JsonResponse({'success': False, 'errors': form.errors})

    # Menyediakan data awal untuk modal
    if request.user.is_resto_owner:
        user_resto = RestaurantOwner.objects.get(user=request.user)
        profile = OwnerProfile.objects.get(user=user_resto)
    elif request.user.is_customer:
        user_customer = Customer.objects.get(user=request.user)
        profile = CustomerProfile.objects.get(user=user_customer)
    else:
        profile = None  # Jika peran lain, profil bisa disesuaikan sesuai kebutuhan

    # Initial data dengan bio dari profil yang sesuai
    initial_data = {
        'username': request.user.username,
        'email': request.user.email,
        'bio': profile.bio if profile else '',  # Mendapatkan bio jika profile ditemukan
    }

    return render(request, 'edit_profile.html', {'initial_data': initial_data})

# @login_required
# @csrf_exempt  
# def edit_owner_profile(request):
#     user_form = UsernameForm(instance=request.user)
#     profile_form = OwnerProfileForm(instance=request.user.ownerprofile)
    
#     if request.method == 'POST':
#         user_form = UsernameForm(request.POST, instance=request.user)
#         profile_form = OwnerProfileForm(request.POST, request.FILES, instance=request.user.ownerprofile)  
        
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             return JsonResponse({'success': True, 'redirect_url': '/my-profile/'})  

#         return JsonResponse({'success': False, 'errors': user_form.errors | profile_form.errors})

#     return JsonResponse({'success': False, 'errors': 'Invalid request method.'})


# def delete_account(request):
#     if request.method == 'POST':
#         user = request.user
        
#         try:
#             customer_profile = CustomerProfile.objects.get(user=user)
#             customer_profile.delete()
#         except CustomerProfile.DoesNotExist:
#             pass
        
#         try:
#             owner_profile = OwnerProfile.objects.get(user=user)
#             owner_profile.delete()
#         except OwnerProfile.DoesNotExist:
#             pass
        
#         user.delete()
        
#         messages.success(request, "Your account has been successfully deleted.")
#         return redirect('main:login') 
    
#     return HttpResponseForbidden("Invalid request method.")

# @login_required
# def bookmarks_view(request):
#     user = request.user
#     customer_profile = CustomerProfile.objects.get(user=user)
#     bookmarks = customer_profile.bookmarks.all()  # Assuming bookmarks is a ManyToManyField

#     return render(request, 'bookmarks.html', {
#         'bookmarks': bookmarks,
#     })

# @login_required
# def review_history_view(request):
#     return redirect('/review/""')
#     user = request.user
#     reviews = Review.objects.filter(user=user) 

#     return render(request, 'all_review.html', {
#         'reviews': reviews,
#     })


# @login_required
# def my_restaurant_view(request):
#     return redirect('/restaurant/""')
#     user = request.user
#     # Get the restaurant owner profile
#     owner_profile = get_object_or_404(OwnerProfile, user=user)
    
#     # Get the associated restaurant
#     restaurant = owner_profile.restaurant
    
#     return render(request, 'restaurant.html', {
#         'restaurant': restaurant,
#     })

# @login_required
# def other_profile_view(request, username):
#     user = get_object_or_404(User, username=username)

#     customer_profile = None
#     owner_profile = None

#     if user.is_customer:
#         customer_profile = get_object_or_404(CustomerProfile, user=user)
#     elif user.is_resto_owner:
#         owner_profile = get_object_or_404(OwnerProfile, user=user)

#     return render(request, 'other_profile.html', {
#         'user': user,
#         'customer_profile': customer_profile,
#         'owner_profile': owner_profile,
#     })