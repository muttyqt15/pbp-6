from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Review

# @login_required
def create_review(request):
    if request.method == 'POST':
        judul = request.POST.get('judul_ulasan')
        teks = request.POST.get('teks_ulasan')
        penilaian = request.POST.get('penilaian')
        gambar = request.FILES.get('gambar')

        # Buat objek review baru
        Review.objects.create(
            customer=request.user,
            judul_ulasan=judul,
            teks_ulasan=teks,
            penilaian=penilaian,
            gambar=gambar
        )
        return redirect('all_reviews')
    return render(request, 'review/create_review.html')

def all_reviews(request):
    reviews = Review.objects.all().order_by('-tanggal')
    context = {
        'reviews': reviews,
    }
    return render(request, 'review/all_reviews.html', context)

def detail(request, id):
    review = get_object_or_404(Review, id=id)
    is_customer = review.customer == request.user
    context = {
        'review': review,
        'is_customer': is_customer,
    }
    return render(request, 'review/detail.html', context)
