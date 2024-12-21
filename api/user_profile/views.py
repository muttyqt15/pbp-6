import json
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from .forms import CustomerProfileForm, OwnerProfileForm, CustomerProfilePictureForm, OwnerProfilePictureForm
from .models import CustomerProfile, OwnerProfile
from api.authentication.models import RestaurantOwner, Customer
from django.core import serializers

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

@login_required
def other_profile_view(request):
    user = request.user
    try:
        if user.is_resto_owner:
            user_resto = RestaurantOwner.objects.get(user=user)
            userNow = OwnerProfile.objects.get(user=user_resto)
            print("ini OWNER")
        else:
            user_customer = Customer.objects.get(user=user)
            userNow = CustomerProfile.objects.get(user=user_customer)

        return render(request, 'my_profile.html', {
            'userNow': userNow
        })
    except OwnerProfile.DoesNotExist:
        # Jika OwnerProfile tidak ada, arahkan ke form untuk membuat profil atau halaman error
        messages.error(request, "Profil pemilik belum tersedia. Silakan buat profil.")
    
    except CustomerProfile.DoesNotExist:
        # Jika CustomerProfile tidak ada, arahkan ke form untuk membuat profil atau halaman error
        messages.error(request, "Profil pelanggan belum tersedia. Silakan buat profil.")

    except RestaurantOwner.DoesNotExist:
        messages.error(request, "Pengguna tidak memiliki restoran yang terkait.")

    except Customer.DoesNotExist:
        messages.error(request, "Pengguna tidak memiliki profil pelanggan yang terkait.")


@login_required
def profile_view(request):
    user = request.user
    try:
        if user.is_resto_owner:
            user_resto = RestaurantOwner.objects.get(user=user)
            userNow = OwnerProfile.objects.get(user=user_resto)
            print("ini OWNER")
        else:
            user_customer = Customer.objects.get(user=user)
            userNow = CustomerProfile.objects.get(user=user_customer)

        return render(request, 'my_profile.html', {
            'userNow': userNow
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
                    # 'updated_username': request.user.username,
                    # 'updated_email': request.user.email,
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
                    # 'updated_username': request.user.username,
                    # 'updated_email': request.user.email,
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

@login_required
def show_json(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User is not authenticated"}, status=401)

    # Get the authenticated user
    user = request.user
    
    try:
        if user.is_customer:
            # Get the customer and their profile
            user_customer = Customer.objects.get(user=user)
            data = CustomerProfile.objects.filter(user=user_customer)  # Return a queryset
        elif user.is_resto_owner:
            # Get the restaurant owner and their profile
            user_resto = RestaurantOwner.objects.get(user=user)
            data = OwnerProfile.objects.filter(user=user_resto)  # Return a queryset
        else:
            return JsonResponse({"error": "Invalid user role"}, status=400)

        # Serialize the data to JSON
        serialized_data = serializers.serialize("json", data)
        return JsonResponse(json.loads(serialized_data), safe=False)
    except ObjectDoesNotExist as e:
        return JsonResponse({"error": str(e)}, status=404)

from django.http import JsonResponse

# def show_json(request):
#     # Ensure the user is authenticated
#     if not request.user.is_authenticated:
#         return JsonResponse({"status": "unauthorized", "message": "User not authenticated"}, status=401)

#     user = request.user

#     if hasattr(user, "is_customer") and user.is_customer:
#         try:
#             user_customer = Customer.objects.get(user=user)
#             data = CustomerProfile.objects.filter(user=user_customer)
#         except Customer.DoesNotExist:
#             return JsonResponse({"status": "error", "message": "Customer not found"}, status=404)

#     elif hasattr(user, "is_resto_owner") and user.is_resto_owner:
#         try:
#             user_resto = RestaurantOwner.objects.get(user=user)
#             data = OwnerProfile.objects.filter(user=user_resto)
#         except RestaurantOwner.DoesNotExist:
#             return JsonResponse({"status": "error", "message": "Restaurant owner not found"}, status=404)

#     else:
#         return JsonResponse({"status": "error", "message": "Invalid user role"}, status=400)

#     # Serialize the data to JSON
#     serialized_data = serializers.serialize("json", data)
#     return JsonResponse({"status": "success", "data": serialized_data}, safe=False)


# @login_required
# def edit_profile_picture(request):
#     if request.method == 'POST':
#         if request.user.is_resto_owner:
#             user_resto = get_object_or_404(RestaurantOwner, user=request.user)
#             profile = get_object_or_404(OwnerProfile, user=user_resto)
#         elif request.user.is_customer:
#             user_customer = get_object_or_404(Customer, user=request.user)
#             profile = get_object_or_404(CustomerProfile, user=user_customer)
#         else:
#             return JsonResponse({'success': False, 'error': 'Invalid user role'})

#         profile.profile_pic = request.FILES.get('profile_pic')
#         profile.save()

#         return JsonResponse({
#             'success': True,
#             'updated_profile_pic_url': profile.profile_pic.url if profile.profile_pic else None,
#         })

#     return JsonResponse({'success': False, 'error': 'Invalid request method'})

from .forms import CustomerProfilePictureForm, OwnerProfilePictureForm

@login_required
def edit_profile_picture(request):
    if request.method == 'POST':
        if request.user.is_resto_owner:
            print("RESTO")
            user_resto = get_object_or_404(RestaurantOwner, user=request.user)
            profile = get_object_or_404(OwnerProfile, user=user_resto)
            form = OwnerProfilePictureForm(request.POST, instance=profile)
        elif request.user.is_customer:
            print("CUST")
            user_customer = get_object_or_404(Customer, user=request.user)
            profile = get_object_or_404(CustomerProfile, user=user_customer)
            form = CustomerProfilePictureForm(request.POST, instance=profile)
        else:
            print("INVALID")
            return JsonResponse({'success': False, 'error': 'Invalid user role'})
            
        if form.is_valid():
            form.save()
            print("FORM VALID")
            return JsonResponse({
                'success': True,
                'updated_profile_pic_url': profile.profile_pic_url,
            })
        else:
            print("FORM INVALID")
            return JsonResponse({'success': False, 'errors': form.errors})

    print("INVALID METHOD")
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt  # Memungkinkan permintaan dari aplikasi eksternal seperti Flutter
@login_required
def edit_profile_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse JSON dari permintaan Flutter

        if request.user.is_resto_owner:
            user_resto = RestaurantOwner.objects.get(user=request.user)
            old_form = OwnerProfile.objects.get(user=user_resto)
            form = OwnerProfileForm(data, request.FILES, instance=old_form)

            if form.is_valid():
                form.save()
                return JsonResponse({
                    'success': True,
                    'updated_bio': old_form.bio,
                    'message': 'Profile updated successfully'
                })
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)

        elif request.user.is_customer:
            user_customer = Customer.objects.get(user=request.user)
            old_form = CustomerProfile.objects.get(user=user_customer)
            form = CustomerProfileForm(data, request.FILES, instance=old_form)

            if form.is_valid():
                form.save()
                return JsonResponse({
                    'success': True,
                    'updated_bio': old_form.bio,
                    'message': 'Profile updated successfully'
                })
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    elif request.method == 'GET':
        # Menyediakan data awal untuk edit profile
        if request.user.is_resto_owner:
            user_resto = RestaurantOwner.objects.get(user=request.user)
            profile = OwnerProfile.objects.get(user=user_resto)
        elif request.user.is_customer:
            user_customer = Customer.objects.get(user=request.user)
            profile = CustomerProfile.objects.get(user=user_customer)
        else:
            return JsonResponse({'success': False, 'message': 'Invalid user role'}, status=400)

        return JsonResponse({
            'success': True,
            'data': {
                'username': request.user.username,
                'email': request.user.email,
                'bio': profile.bio,
            }
        })

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


@csrf_exempt  # Memungkinkan permintaan dari aplikasi eksternal seperti Flutter
@login_required
def delete_account_flutter(request):
    if request.method == 'POST':
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

            return JsonResponse({
                'success': True,
                'message': "Your account has been successfully deleted."
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': "There was an error deleting your account.",
                'error': str(e)
            }, status=500)

    return JsonResponse({'success': False, 'message': "Invalid request method."}, status=405)

@csrf_exempt
@login_required
def fetch_profile(request):
    user = request.user

    try:
        if user.is_customer:
            # Jika pengguna adalah Customer
            customer = Customer.objects.get(user=user)
            profile = CustomerProfile.objects.get(user=customer)
            profile_data = {
                'role': 'customer',
                'username': user.username,
                'email': user.email,
                'bio': profile.bio,
                'profile_pic': profile.profile_pic_url
            }

        elif user.is_resto_owner:
            # Jika pengguna adalah RestaurantOwner
            restaurant_owner = RestaurantOwner.objects.get(user=user)
            profile = OwnerProfile.objects.get(user=restaurant_owner)
            profile_data = {
                'role': 'restaurant_owner',
                'username': user.username,
                'email': user.email,
                'bio': profile.bio,
                'profile_pic': profile.profile_pic_url
            }
        else:
            return JsonResponse({'success': False, 'message': 'User role not recognized'}, status=400)

        return JsonResponse({'success': True, 'profile': profile_data}, status=200)

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt  # Allow requests from external applications like Flutter
@login_required
def edit_profile_picture_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON from the request body
            print("Received data:", data)

            if request.user.is_resto_owner:
                print("User is a restaurant owner")
                user_resto = get_object_or_404(RestaurantOwner, user=request.user)
                profile = get_object_or_404(OwnerProfile, user=user_resto)
                form = OwnerProfilePictureForm(data, instance=profile)
            elif request.user.is_customer:
                print("User is a customer")
                user_customer = get_object_or_404(Customer, user=request.user)
                profile = get_object_or_404(CustomerProfile, user=user_customer)
                form = CustomerProfilePictureForm(data, instance=profile)
            else:
                print("Invalid user role")
                return JsonResponse({'success': False, 'error': 'Invalid user role'})

            if form.is_valid():
                form.save()
                print("Form is valid, profile picture updated")
                return JsonResponse({
                    'success': True,
                    'updated_profile_pic_url': profile.profile_pic_url,
                })
            else:
                print("Form is invalid:", form.errors)
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        except Exception as e:
            print("Exception occurred:", str(e))
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    print("Invalid request method")
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

