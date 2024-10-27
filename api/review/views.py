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
from api.authentication.decorators import customer_only

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
@customer_only()
def main_review(request):
    reviews = Review.objects.filter(customer=request.user.customer).order_by('-tanggal')
    context = {'reviews': reviews}
    return render(request, 'main_review.html', context)

@customer_only()
def create_review(request):
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

@customer_only()
@csrf_exempt
def edit_review_ajax(request, id):
    review = get_object_or_404(Review, id=id, customer=request.user.customer)
    
    # Retrieve data from POST request
    judul_ulasan = request.POST.get("judul_ulasan")
    teks_ulasan = request.POST.get("teks_ulasan")
    penilaian = request.POST.get("penilaian")

    # Update review fields
    if judul_ulasan:
        review.judul_ulasan = judul_ulasan
    if teks_ulasan:
        review.teks_ulasan = teks_ulasan
    if penilaian:
        review.penilaian = int(penilaian)

    # Save the updated review
    review.waktu_edit_terakhir = timezone.now()
    review.save()

    # Return a JSON response
    return JsonResponse({"status": "updated"}, status=200)


# AJAX-only view to delete a review
@require_POST
@customer_only()
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
