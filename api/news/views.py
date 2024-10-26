from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from api.news.forms import BeritaEntryForm
from api.news.models import Berita
from api.authentication.models import RestaurantOwner
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core import serializers
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from api.authentication.decorators import resto_owner_only
from django.contrib.auth.decorators import login_required
import uuid
import os

def show_main(request):
    is_restaurant_owner = RestaurantOwner.objects.filter(user=request.user).exists() if request.user.is_authenticated else False

    if (is_restaurant_owner):
        restaurant_owner = RestaurantOwner.objects.get(user=request.user)
        context = {
            "user": request.user,
            "status_user": is_restaurant_owner,
            "restaurant": restaurant_owner.restaurant,
        }
    else:
        context = {
            "user": request.user,
            "status_user": is_restaurant_owner,
        }
    return render(request, "main_berita.html", context)

@resto_owner_only(redirect_url="/")
def owner_panel(request):
    restaurant_owner = RestaurantOwner.objects.get(user=request.user)
    context = {
            "nama": request.user.username,
            "id": request.user.id,
            "restaurant": restaurant_owner.restaurant,
        }
    return render(request, "owner_panel.html", context)

def serialize_berita(berita, liked):
    """Helper function to serialize Berita data for JSON responses."""
    restaurant = getattr(berita.author, 'restaurant', None)
    return {
        'pk': berita.pk,
        'fields': {
            'judul': berita.judul,
            'gambar': berita.gambar.url if berita.gambar else "",
            'konten': berita.konten,
            'like': berita.like.count(),
            'author': berita.author.user.username,
            'tanggal': berita.tanggal,
            'tanggal_pembaruan': berita.tanggal_pembaruan,
            'liked': liked,
            'data_restaurant': {
                'id': restaurant.id if restaurant else None,
                'name': restaurant.name if restaurant else "",
                'district': restaurant.district if restaurant else "",
                'address': restaurant.address if restaurant else "",
                'operational_hours': restaurant.operational_hours if restaurant else "",
                'photo_url': restaurant.photo_url if restaurant and restaurant.photo_url else ""
            }
        }
    }

def show_berita_json(request):
    try:
        berita_data = [
            serialize_berita(berita, berita.like.filter(id=request.user.id).exists())
            for berita in Berita.objects.all()
        ]
        return JsonResponse(berita_data, safe=False)
    except Exception as e:
        return JsonResponse({"error": f"Error: {str(e)}"}, status=500)

@resto_owner_only(redirect_url="/")
def show_berita_by_owner(request):
    try:
        berita_data = [
            serialize_berita(berita, berita.like.filter(id=request.user.id).exists())
            for berita in Berita.objects.filter(author__user=request.user)
        ]
        return JsonResponse(berita_data, safe=False)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

@resto_owner_only(redirect_url="/")
def edit_berita(request, berita_id):
    try:
        berita = get_object_or_404(Berita, pk=berita_id)
        if request.method == 'POST':
            form = BeritaEntryForm(request.POST, request.FILES, instance=berita)
            if form.is_valid():
                if 'image' in request.FILES:
                    if berita.gambar and os.path.isfile(berita.gambar.path):
                        os.remove(berita.gambar.path)
                    unique_name = f"{uuid.uuid4()}_{request.FILES['image'].name}"
                    berita.gambar = request.FILES['image']
                    berita.gambar.name = unique_name
                berita.tanggal_pembaruan = timezone.now()
                form.save()
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'message': 'Form is not valid'}, status=400)
        return HttpResponse(serializers.serialize('json', [berita]), content_type="application/json")
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@resto_owner_only(redirect_url="/")
def delete_berita(request, berita_id):
    try:
        berita = get_object_or_404(Berita, pk=berita_id)
        if berita.gambar and os.path.isfile(berita.gambar.path):
            os.remove(berita.gambar.path)
        berita.delete()
        return HttpResponseRedirect(reverse('news:show_main'))
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

@csrf_exempt
@require_POST
def add_berita_ajax(request):
    try:
        restaurant_owner = RestaurantOwner.objects.get(user=request.user)
        judul = strip_tags(request.POST.get("judul"))
        gambar = request.FILES.get("gambar")
        konten = strip_tags(request.POST.get("konten"))
        if gambar:
            unique_name = f"{uuid.uuid4()}_{gambar.name}"
            gambar.name = unique_name
        berita = Berita(author=restaurant_owner, judul=judul, gambar=gambar, konten=konten)
        berita.save()
        return HttpResponse(b'CREATED', status=201)
    except RestaurantOwner.DoesNotExist:
        return HttpResponse("User is not a Restaurant Owner.", status=403)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

def like_berita(request, berita_id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": False, "liked": False})
    
    if request.method == "POST":
        berita = get_object_or_404(Berita, pk=berita_id)
        status_liked = request.user in berita.like.all()
        if status_liked:
            berita.like.remove(request.user)
        else:
            berita.like.add(request.user)
        return JsonResponse({"status": True, "likes": berita.like.count(), "liked": not status_liked})
    return HttpResponseForbidden()
