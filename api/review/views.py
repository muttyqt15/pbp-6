import base64
import json
import traceback
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from .forms import ReviewForm
from .models import Review, ReviewImage
from django.db.models import Count
from django.utils import timezone
from django.http import HttpResponseForbidden
from api.restaurant.models import Restaurant
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.utils.html import strip_tags

# Custom decorator to check if the user has a customer profile
def customer_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'customer'):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Only customers can access this page.")
    return _wrapped_view

def login_required_json(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "User not authenticated"}, status=403)
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@require_POST
def like_review_ajax(request, id):
    review = get_object_or_404(Review, pk=id)
    user = request.user

    if user in review.likes.all():
        # If the user has already liked the review, remove the like
        review.likes.remove(user)
        liked = False
    else:
        # Otherwise, add a like
        review.likes.add(user)
        liked = True

    return JsonResponse({
        "liked": liked,
        "total_likes": review.likes.count()
    })

# Main review view for the logged-in user's reviews
@login_required
@customer_required
def main_review(request):
    reviews = Review.objects.filter(customer=request.user.customer).order_by('-tanggal')
    if reviews.exists():
        restaurant_id = reviews.first().restoran.id 
    else:
        restaurant_id = None 

    context = {
        'reviews': reviews,
        'restaurant_id': restaurant_id,
    }
    return render(request, 'main_review.html', context)

@login_required
@customer_required
def create_review(request):
    restaurants = Restaurant.objects.all()
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user.customer  
            review.restoran = form.cleaned_data.get('restaurant')
            review.display_name = form.cleaned_data.get('display_name')
            review.save()

            # Save each uploaded image to ReviewImage
            for img in request.FILES.getlist('images'):
                ReviewImage.objects.create(review=review, image=img)
            
            return redirect('review:main_review')
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = ReviewForm()
    return render(request, 'create_review.html', {'form': form, 'restaurants': restaurants})

@login_required
@customer_required
@csrf_exempt
def edit_review_ajax(request, id):
    review = get_object_or_404(Review, pk=id, customer=request.user.customer)

    # Update review fields from POST data
    review.display_name = request.POST.get("display_name", review.display_name)
    review.judul_ulasan = request.POST.get("judul_ulasan", review.judul_ulasan)
    review.teks_ulasan = request.POST.get("teks_ulasan", review.teks_ulasan)
    review.penilaian = request.POST.get("penilaian", review.penilaian)

    # Save the updated review
    review.save()

    # Return the updated fields as JSON, including all needed context
    return JsonResponse({
        "display_name": review.display_name,
        "judul_ulasan": review.judul_ulasan,
        "teks_ulasan": review.teks_ulasan,
        "penilaian": review.penilaian,
        "tanggal": review.tanggal.strftime('%d %B %Y'),
    })

# AJAX-only view to delete a review
@login_required
@require_POST
@customer_required
@csrf_protect
def delete_review_ajax(request, id):
    review = get_object_or_404(Review, pk=id, customer=request.user.customer)
    review.delete()
    return JsonResponse({"success": True})

# JSON view for all reviews
def show_json(request):
    reviews = Review.objects.all()
    serialized_data = serializers.serialize("json", reviews)
    data_list = json.loads(serialized_data)

    # Tambahkan field images secara manual
    for obj in data_list:
        review_id = obj['pk']
        review = get_object_or_404(Review, pk=review_id)
        # Kumpulkan URL dari ReviewImage terkait
        images = [image.image.url for image in review.images.all()]
        obj['fields']['images'] = images

    return JsonResponse(data_list, safe=False)

# JSON view for a specific review by ID
def show_json_by_id(request, id):
    reviews = Review.objects.filter(pk=id)
    serialized_data = serializers.serialize("json", reviews)
    data_list = json.loads(serialized_data)

    # Tambahkan field images secara manual
    for obj in data_list:
        review_id = obj['pk']
        review = get_object_or_404(Review, pk=review_id)
        images = [image.image.url for image in review.images.all()]
        obj['fields']['images'] = images

    return JsonResponse(data_list, safe=False)

# Create a review (Flutter-specific)
@login_required
@csrf_exempt
def user_reviews_flutter(request):
    try:
        user = request.user.customer
        reviews = Review.objects.filter(customer=user).annotate(total_likes_count=Count('likes')).order_by('-tanggal')

        review_list = [
            {
                "id": str(review.pk),
                "restoran_name": review.restoran.name if review.restoran else "Nama Restoran",
                "judul_ulasan": review.judul_ulasan,
                "teks_ulasan": review.teks_ulasan,
                "penilaian": review.penilaian,
                "tanggal": review.tanggal.strftime('%Y-%m-%d'),
                "display_name": review.get_display_name, 
                "total_likes": review.total_likes_count,  
                "images": [
                    request.build_absolute_uri(image.image.url) for image in review.images.all()
                ],
            }
            for review in reviews
        ]

        return JsonResponse({"status": "success", "data": review_list}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
    

@csrf_exempt
@login_required_json
def create_review_flutter(request):
    if request.method == 'POST':
        try:
            # Parse body JSON
            data = json.loads(request.body)

            display_name = data.get('display_name', None)
            restoran_id = data.get('restoran_id')
            judul_ulasan = data.get('judul_ulasan')
            teks_ulasan = data.get('teks_ulasan')
            penilaian = data.get('penilaian')

            # Validasi input
            if not all([restoran_id, judul_ulasan, teks_ulasan, penilaian]):
                return JsonResponse({"status": "error", "message": "All fields except display_name are required."}, status=400)

            restoran = get_object_or_404(Restaurant, id=restoran_id)

            # Buat review baru
            new_review = Review.objects.create(
                customer=request.user.customer,
                restoran=restoran,
                judul_ulasan=judul_ulasan,
                teks_ulasan=teks_ulasan,
                penilaian=int(penilaian),
                display_name=display_name,
            )

            # Handle image (optional)
            # Proses image_base64 jika tersedia
            image_base64 = data.get('image_base64', None)
            if image_base64:
                # Tentukan ekstensi berdasarkan prefix base64
                if image_base64.startswith('data:image/png;base64,'):
                    ext = 'png'
                    image_base64 = image_base64.replace('data:image/png;base64,', '')
                elif image_base64.startswith('data:image/jpeg;base64,') or image_base64.startswith('data:image/jpg;base64,'):
                    ext = 'jpg'
                    image_base64 = image_base64.replace('data:image/jpeg;base64,', '').replace('data:image/jpg;base64,', '')
                else:
                    ext = 'png'  # Default ke PNG jika tipe tidak dikenali

                # Decode base64 dan simpan file
                image_data = base64.b64decode(image_base64)
                filename = f"uploaded_image_{new_review.pk}.{ext}"  # Nama file unik berdasarkan ID review
                ReviewImage.objects.create(
                    review=new_review,
                    image=ContentFile(image_data, name=filename)
                )
            return JsonResponse({"status": "success", "message": "Review created successfully."}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON input."}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid HTTP method."}, status=405)

@login_required
@csrf_exempt
@require_http_methods(["POST", "GET"])
def edit_review_flutter(request, review_id):
    try:
        # Verify review ownership
        review = get_object_or_404(Review, id=review_id, customer=request.user.customer)

        if request.method == "POST":
            try:
                data = json.loads(request.body)

                # Update fields
                review.judul_ulasan = data.get("judul_ulasan", review.judul_ulasan)
                review.teks_ulasan = strip_tags(data.get("teks_ulasan", review.teks_ulasan))
                review.penilaian = int(data.get("penilaian", review.penilaian))
                review.display_name = data.get("display_name", review.display_name)

                # Handle new image
                if "new_image_base64" in data and data["new_image_base64"]:
                    image_data = base64.b64decode(data["new_image_base64"].split(",")[1])
                    filename = f"review_{review.id}.jpeg"
                    ReviewImage.objects.create(
                        review=review,
                        image=ContentFile(image_data, name=filename),
                    )

                # Save updated review
                review.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Review updated successfully.",
                    "data": {
                        "judul_ulasan": review.judul_ulasan,
                        "teks_ulasan": review.teks_ulasan,
                        "penilaian": review.penilaian,
                        "display_name": review.display_name,
                        "images": [image.image.url for image in review.images.all()],
                    },
                })
            except json.JSONDecodeError:
                return JsonResponse({"status": "error", "message": "Invalid JSON format."}, status=400)
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=500)
        
        # GET request to return current review details
        return JsonResponse({
            "status": "success",
            "data": {
                "judul_ulasan": review.judul_ulasan,
                "teks_ulasan": review.teks_ulasan,
                "penilaian": review.penilaian,
                "display_name": review.display_name,
                "images": [image.image.url for image in review.reviewimage_set.all()],
            },
        })
    except Review.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Review not found."}, status=404)


# Delete a review (Flutter-specific)
@csrf_exempt
@require_http_methods(["POST", "DELETE"])
@login_required
def delete_review_flutter(request, review_id):
    try:
        # Periksa apakah user memiliki role customer
        if not hasattr(request.user, 'customer'):
            return JsonResponse(
                {"status": "error", "message": "Only customers can delete reviews."},
                status=403,
            )

        # Ambil ulasan berdasarkan ID
        review = get_object_or_404(Review, id=review_id)

        # Pastikan ulasan milik customer yang sedang login
        if review.customer.user != request.user:
            return JsonResponse(
                {"status": "error", "message": "You are not authorized to delete this review."},
                status=403,
            )

        # Hapus ulasan
        review.delete()
        return JsonResponse(
            {"status": "success", "message": "Review deleted successfully."},
            status=200,
        )

    except Review.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Review not found."},
            status=404,
        )

    except Exception as e:
        return JsonResponse(
            {"status": "error", "message": str(e)},
            status=500,
        )
    
def all_restaurants_flutter(request):
    if request.method == "GET":
        restaurants = Restaurant.objects.all()
        data = [
            {
                "pk": restaurant.pk,
                "fields": {
                    "name": restaurant.name,
                    "district": restaurant.district,
                    "address": restaurant.address,
                    "operational_hours": restaurant.operational_hours,
                    "photo_url": restaurant.photo_url,
                },
            }
            for restaurant in restaurants
        ]
        return JsonResponse(data, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=400)