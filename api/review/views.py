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
from api.authentication.models import Customer
import json
import base64
from django.core.files.base import ContentFile

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
# def show_json(request):
#     data = Review.objects.all()
#     return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json(request):
    reviews = Review.objects.all()  # Ambil semua review
    data = []
    for review in reviews:
        review_data = {
            "id": str(review.id),
            "judul_ulasan": review.judul_ulasan,
            "teks_ulasan": review.teks_ulasan,
            "penilaian": review.penilaian,
            "tanggal": review.tanggal,
            "total_likes": review.total_likes,
            "images": [image.image.url for image in review.images.all()],  # Semua URL gambar terkait
        }
        data.append(review_data)
    
    return JsonResponse(data, safe=False)


# JSON view for a specific review by ID
def show_json_by_id(request, id):
    data = Review.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required
@customer_required
@csrf_exempt
def create_review_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            restoran_id = data.get("restoran_id")
            judul_ulasan = data.get("judul_ulasan")
            teks_ulasan = data.get("teks_ulasan")
            penilaian = data.get("penilaian")
            display_name = data.get("display_name", "")
            images = data.get("images", [])  # Expecting a list of base64 strings

            # Validate required fields
            if not judul_ulasan or not teks_ulasan or not penilaian:
                return JsonResponse({"status": "error", "message": "Missing required fields."}, status=400)

            # Get customer from request.user
            customer = request.user.customer

            # Get Restaurant if restoran_id is provided
            restoran = get_object_or_404(Restaurant, id=restoran_id) if restoran_id else None

            # Create Review
            new_review = Review.objects.create(
                customer=customer,
                restoran=restoran,
                judul_ulasan=judul_ulasan,
                teks_ulasan=teks_ulasan,
                penilaian=penilaian,
                display_name=display_name
            )

            # Handle base64-encoded images
            for img_str in images:
                try:
                    format, imgstr = img_str.split(';base64,') 
                    ext = format.split('/')[-1] 
                    image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                    ReviewImage.objects.create(review=new_review, image=image)
                except Exception as e:
                    return JsonResponse({"status": "error", "message": f"Image upload failed: {str(e)}"}, status=400)

            return JsonResponse({"status": "success", "review_id": str(new_review.id)}, status=201)

        except Restaurant.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Restaurant not found."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON."}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Invalid HTTP method."}, status=405)
    
@login_required
def review_detail(request, product_id):
    review = get_object_or_404(Review, pk=product_id)
    review_data = {
        "id": str(review.id),
        "judul_ulasan": review.judul_ulasan,
        "teks_ulasan": review.teks_ulasan,
        "penilaian": review.penilaian,
        "tanggal": review.tanggal.strftime('%Y-%m-%d'),
        "total_likes": review.total_likes,
        "images": [image.image.url for image in review.images.all()],
        "display_name": review.get_display_name,
    }
    return JsonResponse(review_data, status=200)