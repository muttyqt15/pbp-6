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

# Custom decorator to check if the user has a customer profile
def customer_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'customer'):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Only customers can access this page.")
    return _wrapped_view

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

def all_review(request):
    # Retrieve all reviews, ordered by likes and last edited time
    reviews = (
        Review.objects.all()
        .annotate(num_likes=Count('likes'))
        .order_by('-num_likes', '-waktu_edit_terakhir')
    )
    
    context = {
        'all_reviews': reviews,
    }
    print(context)
    return render(request, 'all_review.html', context)

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
        "tanggal": review.tanggal.strftime('%Y-%m-%d'),
        # Add any additional context fields here if needed
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
        sort_by = request.GET.get('sort_by', '')  # Ambil parameter sort_by

        # Ambil review milik user dan hitung jumlah likes (gunakan nama lain)
        reviews = Review.objects.filter(customer=user).annotate(total_likes_count=Count('likes'))

        # Sorting berdasarkan parameter
        if sort_by == "like":
            reviews = reviews.order_by('-total_likes_count')
        elif sort_by == "rate":
            reviews = reviews.order_by('-penilaian')
        elif sort_by == "date":
            reviews = reviews.order_by('-tanggal')
        else:
            reviews = reviews.order_by('-tanggal')

        # Format data JSON sesuai dengan Flutter model
        review_list = [
            {
                "id": str(review.pk),
                "restoran_name": review.restoran.name if review.restoran else "Nama Restoran",
                "judul_ulasan": review.judul_ulasan,
                "teks_ulasan": review.teks_ulasan,
                "penilaian": review.penilaian,
                "tanggal": review.tanggal.strftime('%Y-%m-%d'),
                "display_name": review.get_display_name,  # Ambil dari properti get_display_name
                "total_likes": review.total_likes_count,  # Gunakan hasil annotate
                "images": [image.image.url for image in review.images.all()],
            }
            for review in reviews
        ]

        return JsonResponse({"status": "success", "data": review_list}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

    
@login_required
@csrf_exempt
def create_review_flutter(request):
    if request.method == 'POST':
        try:
            # Mengambil data teks
            display_name = request.POST.get('display_name', '')
            restoran_id = request.POST.get('restoran_id')
            judul_ulasan = request.POST.get('judul_ulasan')
            teks_ulasan = request.POST.get('teks_ulasan')
            penilaian = request.POST.get('penilaian')

            # Validasi input wajib
            if not (judul_ulasan and teks_ulasan and penilaian and restoran_id):
                return JsonResponse({"status": "error", "message": "Semua field wajib diisi."}, status=400)

            # Validasi penilaian
            try:
                penilaian = int(penilaian)
                if penilaian < 1 or penilaian > 5:
                    raise ValueError
            except ValueError:
                return JsonResponse({"status": "error", "message": "Penilaian harus antara 1-5"}, status=400)

            # Validasi restoran
            restoran = get_object_or_404(Restaurant, id=restoran_id)

            # Buat review baru
            new_review = Review.objects.create(
                customer=request.user.customer,
                restoran=restoran,
                judul_ulasan=judul_ulasan,
                teks_ulasan=teks_ulasan,
                penilaian=penilaian,
                display_name=display_name
            )

            # Handle file upload
            images = request.FILES.getlist('images')
            for image in images:
                ReviewImage.objects.create(review=new_review, image=image)

            return JsonResponse({"status": "success", "message": "Review berhasil dibuat."}, status=201)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid HTTP method."}, status=405)

@login_required
@csrf_exempt
def edit_review_flutter(request, id):
    try:
        review = get_object_or_404(Review, pk=id, customer=request.user.customer)

        if request.method == 'POST':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"status": "error", "message": "Invalid JSON format."}, status=400)

            new_penilaian = data.get("penilaian", review.penilaian)
            if new_penilaian is not None:
                try:
                    new_penilaian = int(new_penilaian)
                    if new_penilaian < 1 or new_penilaian > 5:
                        raise ValueError
                except ValueError:
                    return JsonResponse({"status": "error", "message": "Penilaian harus antara 1-5"}, status=400)

            review.judul_ulasan = data.get("judul_ulasan", review.judul_ulasan)
            review.teks_ulasan = data.get("teks_ulasan", review.teks_ulasan)
            review.penilaian = new_penilaian
            review.display_name = data.get("display_name", review.display_name)

            review.save()

            return JsonResponse({"status": "success", "message": "Review updated successfully."}, status=200)

        return JsonResponse({"status": "error", "message": "Invalid HTTP method."}, status=405)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

# Delete a review (Flutter-specific)
@login_required
@csrf_exempt
def delete_review_flutter(request, id):
    try:
        review = get_object_or_404(Review, pk=id, customer=request.user.customer)
        if request.method == 'DELETE':
            review.delete()
            return JsonResponse({"status": "success", "message": "Review deleted successfully."}, status=200)
        return JsonResponse({"status": "error", "message": "Invalid HTTP method."}, status=405)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

# List all reviews (Flutter-specific)
@csrf_exempt
def list_reviews_flutter(request):
    try:
        page_number = request.GET.get('page', 1)  # Nomor halaman
        reviews = Review.objects.all().annotate(total_likes=Count('likes')).order_by('-tanggal')

        paginator = Paginator(reviews, 10)  # 10 reviews per halaman
        page_obj = paginator.get_page(page_number)

        review_list = [
            {
                "id": str(review.id),
                "judul_ulasan": review.judul_ulasan,
                "teks_ulasan": review.teks_ulasan,
                "penilaian": review.penilaian,
                "tanggal": review.tanggal.strftime('%Y-%m-%d'),
                "total_likes": review.total_likes,
                "images": [image.image.url for image in review.images.all()],
            }
            for review in page_obj
        ]

        return JsonResponse({
            "status": "success",
            "data": review_list,
            "page": page_number,
            "total_pages": paginator.num_pages,
        }, status=200)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

# Like/Unlike a review (Flutter-specific)
@login_required
@csrf_exempt
def like_review_flutter(request, id):
    try:
        review = get_object_or_404(Review, pk=id)
        customer = request.user.customer
        if request.method == 'POST':
            # Jika sudah like, maka unlike. Jika belum, maka like.
            if review.likes.filter(pk=customer.pk).exists():
                review.likes.remove(customer)
                message = "Review unliked."
            else:
                review.likes.add(customer)
                message = "Review liked."

            return JsonResponse({
                "status": "success",
                "message": message,
                "total_likes": review.likes.count()
            }, status=200)
        else:
            return JsonResponse({"status": "error", "message": "Invalid HTTP method."}, status=405)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)