from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .forms import ReviewForm
from .models import Review, ReviewImage

def all_review(request):
    review = Review.objects.all().order_by('-tanggal')
    context = {'review': review}
    return render(request, 'all_review.html', context)

def main_review(request):
    reviews = Review.objects.all().order_by('-tanggal')
    context = {'reviews': reviews}
    return render(request, 'main_review.html', context)

def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()

            # Menyimpan gambar yang diupload jika ada
            gambar = request.FILES.getlist('gambar')
            for img in gambar:
                ReviewImage.objects.create(review=review, image=img)

            return redirect('review:main_review')
    else:
        form = ReviewForm()

    context = {'form': form}
    return render(request, 'create_review.html', context)

def edit_review(request, id):
    review = get_object_or_404(Review, id=id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})  # Mengirim respon sukses ke AJAX
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ReviewForm(instance=review)

    return render(request, 'edit_review.html', {'form': form, 'review': review})

def delete_review(request, id):
    review = get_object_or_404(Review, id=id)

    if request.method == 'POST':
        review.delete()
        return redirect('review:main_review')

def show_json(request):
    data = Review.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = Review.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
