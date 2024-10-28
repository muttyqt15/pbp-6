from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from .forms import ReviewForm
from .models import Review, ReviewImage
from django.db.models import Count
from django.utils import timezone


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

def all_review(request, id):
    # Retrieve all reviews, ordered by likes and last edited time
    reviews = (
        Review.objects.filter(customer=request.user.customer, restoran=request.restoran_id)
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
    context = {'reviews': reviews}
    return render(request, 'main_review.html', context)

@login_required
@customer_required
def create_review(request, id):
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user.customer  # Link to the customer
            review.display_name = form.cleaned_data.get('display_name')
            review.save()

            # Save each uploaded image to ReviewImage
            for img in request.FILES.getlist('images'):
                ReviewImage.objects.create(review=review, image=img)
            
            return redirect('review:main_review')
    else:
        form = ReviewForm()
    return render(request, 'create_review.html', {'form': form})

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
    data = Review.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# JSON view for a specific review by ID
def show_json_by_id(request, id):
    data = Review.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")