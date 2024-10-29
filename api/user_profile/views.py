from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from .forms import CustomerProfileForm, OwnerProfileForm
from .models import CustomerProfile, OwnerProfile
from api.authentication.models import RestaurantOwner, Customer



@login_required
def profile_view(request):
    user = request.user
    try:
        if user.is_resto_owner:
            user_resto = RestaurantOwner.objects.get(user=user)
            userNow = OwnerProfile.objects.get(user=user_resto)
        else:
            user_customer = Customer.objects.get(user=user)
            userNow = CustomerProfile.objects.get(user=user_customer)
        print(user_resto)
        return render(request, 'my_profile.html', {
            'user_resto': user_resto, 'user': user
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

