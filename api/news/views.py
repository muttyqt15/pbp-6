import json
from django.core.files import File
from django.shortcuts import render, get_object_or_404
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
import uuid
import os
import base64
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required

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

@resto_owner_only(redirect_url="/news/")
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

# @resto_owner_only(redirect_url="/news/")
def show_berita_by_owner(request):
    try:
        berita_data = [
            serialize_berita(berita, berita.like.filter(id=request.user.id).exists())
            for berita in Berita.objects.filter(author__user=request.user)
        ]
        return JsonResponse(berita_data, safe=False)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

@resto_owner_only(redirect_url="/news/")
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
                return JsonResponse({'status': 'success'}, status=200)
            return JsonResponse({'status': 'error', 'message': 'Form is not valid'}, status=400)
        return HttpResponse(serializers.serialize('json', [berita]), content_type="application/json")
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=404)

@resto_owner_only(redirect_url="/news/")
def delete_berita(request, berita_id):
    try:
        berita = get_object_or_404(Berita, pk=berita_id)
        if berita.gambar and os.path.isfile(berita.gambar.path):
            os.remove(berita.gambar.path)
        berita.delete()
        return HttpResponseRedirect(reverse('news:show_main'))
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

@resto_owner_only(redirect_url="/news/")
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
    

@csrf_exempt
def flike_berita(request, berita_id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": False, "logged_in": False, "liked": False})
    
    if request.method == "POST":
        berita = get_object_or_404(Berita, pk=berita_id)
        status_liked = request.user in berita.like.all()
        if status_liked:
            berita.like.remove(request.user)
        else:
            berita.like.add(request.user)
        return JsonResponse({
            "status": True,
            "logged_in": True,
            "liked": not status_liked,
            "likes": berita.like.count()
        })
    return JsonResponse({"status": False, "logged_in": False}, status=405)



def fdelete_berita(request, berita_id):
    if request.method == "GET":
        try:
            berita = Berita.objects.get(pk=berita_id)
            if berita.gambar and os.path.isfile(berita.gambar.path):
                os.remove(berita.gambar.path)
            berita.delete()
            return JsonResponse({"status": 200, "message": "Berita deleted successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def fshow_berita_id(request, berita_id):
    try:
        berita = get_object_or_404(Berita, pk=berita_id)
        liked = berita.like.filter(id=request.user.id).exists() if request.user.is_authenticated else False
        berita_data = serialize_berita(berita, liked)
        return JsonResponse(berita_data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
        
@csrf_exempt
def fadd_berita_ajax(request):
    print("DEBUG: Received cookies:", request.COOKIES)
    if not request.user.is_authenticated:
        print("ERROR: User not authenticated.")
        return JsonResponse({"status": 401, "message": "User not authenticated."}, status=401)

    if request.method == 'POST':
        try:
            judul = strip_tags(request.POST.get("judul"))
            konten = strip_tags(request.POST.get("konten"))
            gambar_file = request.FILES.get("gambar")  # Untuk file multipart
            gambar_base64 = request.POST.get("gambar_base64")  # Untuk gambar base64

            print("DEBUG: Judul:", judul)
            print("DEBUG: Konten:", konten)

            if not judul or not konten:
                print("ERROR: Judul atau Konten kosong.")
                return JsonResponse({"status": 400, "message": "Judul dan Konten tidak boleh kosong."}, status=400)

            restaurant_owner = RestaurantOwner.objects.get(user=request.user)
            print("DEBUG: RestaurantOwner ditemukan:", restaurant_owner)

            # Simpan berita tanpa gambar terlebih dahulu untuk mendapatkan ID
            berita = Berita(
                author=restaurant_owner,
                judul=judul,
                konten=konten
            )
            berita.save()

            # Proses gambar jika ada
            if gambar_base64:
                format, imgstr = gambar_base64.split(';base64,') if ';base64,' in gambar_base64 else (None, gambar_base64)
                ext = format.split('/')[-1] if format else 'png'
                gambar_name = f"berita_{berita.id}_{timezone.now().date()}_{timezone.now().time()}.{ext}"
                gambar = ContentFile(base64.b64decode(imgstr), name=gambar_name)
                berita.gambar = gambar
            elif gambar_file:
                ext = gambar_file.name.split('.')[-1]
                gambar_name = f"berita_{berita.id}.{ext}"
                gambar_file.name = gambar_name
                berita.gambar = gambar_file
            else:
                # Gunakan dummy image jika tidak ada gambar
                berita.gambar = 'news/dummy.jpg'

            # Simpan ulang berita dengan gambar
            berita.save()
            print("DEBUG: Berita berhasil disimpan dengan ID:", berita.id)

            return JsonResponse({"status": 200, "message": "Berita berhasil dibuat"}, status=200)

        except RestaurantOwner.DoesNotExist:
            print(f"ERROR: User {request.user} bukan RestaurantOwner.")
            return JsonResponse({"status": 403, "message": "User is not a Restaurant Owner."}, status=403)
        except Exception as e:
            print("ERROR: Exception saat menangani request:", str(e))
            return JsonResponse({"status": 500, "message": f"Error: {str(e)}"}, status=500)

    print("ERROR: Metode request tidak valid.")
    return JsonResponse({"status": 405, "message": "Invalid method."}, status=405)

@csrf_exempt
def fedit_berita(request, berita_id):
    try:
        berita = get_object_or_404(Berita, pk=berita_id)

        if request.method == 'POST':
            judul = strip_tags(request.POST.get("judul"))
            konten = strip_tags(request.POST.get("konten"))
            gambar_file = request.FILES.get("gambar")  # Untuk file multipart
            gambar_base64 = request.POST.get("gambar_base64")  # Untuk gambar base64

            # Validasi judul dan konten
            if not judul or not konten:
                return JsonResponse(
                    {"status": 400, "message": "Judul dan Konten wajib diisi."},
                    status=400,
                )

            # Update judul dan konten
            berita.judul = judul
            berita.konten = konten

            # Proses gambar baru jika ada
            if gambar_base64:
                # Decode base64 dan simpan sebagai file
                format, imgstr = gambar_base64.split(';base64,') if ';base64,' in gambar_base64 else (None, gambar_base64)
                ext = format.split('/')[-1] if format else 'png'
                gambar = ContentFile(base64.b64decode(imgstr), name=f"berita_{berita.id}_{timezone.now().date()}_{timezone.now().time()}.{ext}")
                if berita.gambar:
                    berita.gambar.delete()  # Hapus gambar lama
                berita.gambar = gambar
            elif gambar_file:
                # Simpan file gambar baru
                if berita.gambar:
                    berita.gambar.delete()  # Hapus gambar lama
                berita.gambar = gambar_file
            # Jika tidak ada gambar baru, biarkan gambar yang lama tetap ada
            else:
                print("DEBUG: Tidak ada perubahan pada gambar.")

            berita.save()
            return JsonResponse({"status": 200, "message": "Berita berhasil diperbarui"}, status=200)

        return JsonResponse({"status": 405, "message": "Invalid method."}, status=405)

    except Exception as e:
        return JsonResponse({"status": 500, "message": f"Error: {str(e)}"}, status=500)

@csrf_exempt
def get_user_role(request):
    print(request)
    try:
        restaurant_owner = RestaurantOwner.objects.get(user=request.user)
        if restaurant_owner:
            return JsonResponse({
                "status": 200,
                "role": "restaurant_owner",
                "is_owner": True
            })
        else:
            return JsonResponse({
                "status": 200,
                "role": "customer",
                "is_owner": False
            })
    except Exception as e:
        return JsonResponse({"status": 500, "message": f"Error: {str(e)}"}, status=500)