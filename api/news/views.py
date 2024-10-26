# from django.shortcuts import render, redirect, get_object_or_404
# from django.urls import reverse
# from api.news.forms import BeritaEntryForm
# from api.news.models import Berita
# from api.authentication.models import RestaurantOwner
# from django.http import HttpResponseRedirect
# from django.http import HttpResponse
# from django.core import serializers
# from django.utils import timezone
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_POST
# from django.utils.html import strip_tags
# from django.http import JsonResponse, HttpResponseForbidden
# from api.authentication.decorators import resto_owner_only
# from django.contrib.auth.decorators import login_required
# import uuid
# import os



# def show_main(request):
#     context = {
#         'name': 'Mangan" Solo'
#     }
#     return render(request, "main_berita.html", context)

# @resto_owner_only(redirect_url="/")
# def owner_panel(request):
#     context = {
#         'nama': request.user.username,
#         'id': request.user.id,
#     }
#     return render(request, "owner_panel.html", context)

# def show_berita_json(request):
#     berita_list = []
#     try:
#         data = Berita.objects.all()
#         for berita in data:
#             # Mengecek apakah user sudah like
#             liked = berita.like.filter(id=request.user.id).exists()
#             print(berita.author.user.username)
            
#             # Memastikan data restaurant tersedia
#             restaurant = berita.author.restaurant if hasattr(berita.author, 'restaurant') else None
            
#             # Membuat respons data berita
#             berita_data = {
#                 'pk': berita.pk,
#                 'fields': {
#                     'judul': berita.judul,
#                     'gambar': berita.gambar.url,
#                     'konten': berita.konten,
#                     'like': berita.like.count(),
#                     'author': berita.author.user.username,
#                     'tanggal': berita.tanggal,
#                     'tanggal_pembaruan': berita.tanggal_pembaruan,
#                     'liked': liked,
#                     'data_restaurant': {
#                         'id': restaurant.id if restaurant else None,
#                         'name': restaurant.name if restaurant else "",
#                         'district': restaurant.district if restaurant else "",
#                         'address': restaurant.address if restaurant else "",
#                         'operational_hours': restaurant.operational_hours if restaurant else "",
#                         'photo_url': restaurant.photo_url if restaurant and restaurant.photo_url else ""
#                     }
#                 }
#             }
#             berita_list.append(berita_data)
        
#         return JsonResponse(berita_list, safe=False)
    
#     except Exception as e:
#         # Mengembalikan pesan error yang lebih detail
#         error_message = f"Error: {str(e)}"
#         return JsonResponse({"error": error_message}, status=500)

# def show_berita_by_id(request, berita_id):
#     try:
#         data = Berita.objects.filter(id=berita_id)
#         if not data.exists():
#             return HttpResponse("Berita with this ID not found", status=404)
#         return HttpResponse(serializers.serialize("json", data), content_type="application/json")
#     except Exception as e:
#         # Menangani error tak terduga dan mengirimkan respons status 500
#         return HttpResponse(f"Error: {str(e)}", status=500)


# @resto_owner_only(redirect_url="/")
# def show_berita_by_owner(request):
#     berita_list = []
#     try:
#         # Filter berita hanya untuk pengguna yang sedang login
#         data = Berita.objects.filter(author_id=request.user.id)
        
#         # # Iterasi setiap berita yang difilter
#         for berita in data:
#             liked = berita.like.filter(id=request.user.id).exists()  # Mengecek apakah user sudah like
#             # Menambahkan berita ke dalam list dengan detail yang diperlukan
#             berita_list.append({
#                 'pk': berita.pk,
#                 'fields': {
#                     'judul': berita.judul,
#                     'gambar': berita.gambar.url,
#                     'konten': berita.konten,
#                     'like': berita.like.count(),  # Menghitung jumlah likes
#                     'author': berita.author.user.username,  # Menampilkan username dari author
#                     'tanggal': berita.tanggal,
#                     'tanggal_pembaruan': berita.tanggal_pembaruan,
#                     'liked': liked  # Status like dari pengguna
#                 }
#             })

#         # Mengembalikan data sebagai JSON
#         return JsonResponse(berita_list, safe=False)
#     except Exception as e:
#         return HttpResponse(f"Error: {str(e)}", status=500)

# # @resto_owner_only(redirect_url="/")
# # def edit_berita(request, berita_id):
# #     try:
# #         berita = Berita.objects.get(pk=berita_id)
        
# #         if request.method == 'POST':
# #             form = BeritaEntryForm(request.POST, request.FILES, instance=berita)

# #             if form.is_valid():
# #                 # Hanya hapus gambar lama jika ada gambar baru yang diunggah
# #                 if 'image' in request.FILES:
# #                     if berita.gambar and os.path.isfile(berita.gambar.path):
# #                         os.remove(berita.gambar.path)
# #                     berita.gambar = request.FILES['image']
                
# #                 # Update tanggal pembaruan
# #                 berita.tanggal_pembaruan = timezone.now()
# #                 form.save()

# #                 return JsonResponse({'status': 'success'})
# #             else:
# #                 return JsonResponse({'status': 'error', 'message': 'Form is not valid'}, status=400)

# #         # Jika GET request, kembalikan data dalam format JSON untuk diisi ke modal
# #         berita_data = serializers.serialize('json', [berita])
# #         return HttpResponse(berita_data, content_type="application/json")

# #     except Berita.DoesNotExist:
# #         return JsonResponse({'status': 'error', 'message': 'Berita not found'}, status=404)
# #     except Exception as e:
# #         return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
# @resto_owner_only(redirect_url="/")
# def edit_berita(request, berita_id):
#     try:
#         berita = Berita.objects.get(pk=berita_id)

#         if request.method == 'POST':
#             form = BeritaEntryForm(request.POST, request.FILES, instance=berita)

#             if form.is_valid():
#                 # Hanya hapus gambar lama jika ada gambar baru yang diunggah
#                 if 'image' in request.FILES:
#                     if berita.gambar and os.path.isfile(berita.gambar.path):
#                         os.remove(berita.gambar.path)

#                     # Ubah nama file menjadi unik
#                     new_image = request.FILES['image']
#                     unique_name = f"{uuid.uuid4()}_{new_image.name}"
#                     new_image.name = unique_name
#                     berita.gambar = new_image

#                 berita.tanggal_pembaruan = timezone.now()
#                 form.save()

#                 return JsonResponse({'status': 'success'})
#             else:
#                 return JsonResponse({'status': 'error', 'message': 'Form is not valid'}, status=400)

#         berita_data = serializers.serialize('json', [berita])
#         return HttpResponse(berita_data, content_type="application/json")

#     except Berita.DoesNotExist:
#         return JsonResponse({'status': 'error', 'message': 'Berita not found'}, status=404)
#     except Exception as e:
#         return JsonResponse({'status': 'error', 'message': str(e)}, status=500)



# @resto_owner_only(redirect_url="/")
# def delete_berita(request, berita_id):
#     try:
#         berita = Berita.objects.get(pk=berita_id)
        
#         # Hapus image jika ada
#         if berita.gambar and os.path.isfile(berita.gambar.path):
#             os.remove(berita.gambar.path)

#         berita.delete()
#         return HttpResponseRedirect(reverse('news:show_main'))
    
#     except Berita.DoesNotExist:
#         return HttpResponse("Berita not found", status=404)
#     except Exception as e:
#         return HttpResponse(f"Error: {str(e)}", status=500)

# # @csrf_exempt
# # @require_POST
# # def add_berita_ajax(request):
# #     try:
# #         # Ambil user yang sedang terautentikasi
# #         user = request.user

# #         # Periksa apakah user adalah restoran owner
# #         restaurant_owner = RestaurantOwner.objects.get(user=user)

# #         judul = strip_tags(request.POST.get("judul"))
# #         gambar = request.FILES.get("gambar")
# #         konten = strip_tags(request.POST.get("konten"))

# #         # Buat instance Berita dan set author sebagai restaurant_owner
# #         berita = Berita(author=restaurant_owner, judul=judul, gambar=gambar, konten=konten)
# #         berita.save()

# #         return HttpResponse(b'CREATED', status=201)
# #     except RestaurantOwner.DoesNotExist:
# #         return HttpResponse("User is not a Restaurant Owner.", status=403)
# #     except Exception as e:
# #         # Kirim respons error ke frontend
# #         return HttpResponse(f"Error: {str(e)}", status=500)

# @csrf_exempt
# @require_POST
# def add_berita_ajax(request):
#     try:
#         user = request.user
#         restaurant_owner = RestaurantOwner.objects.get(user=user)

#         judul = strip_tags(request.POST.get("judul"))
#         gambar = request.FILES.get("gambar")
#         konten = strip_tags(request.POST.get("konten"))

#         # Ubah nama gambar jika ada file yang diunggah
#         if gambar:
#             # Generate UUID untuk nama unik
#             unique_name = f"{uuid.uuid4()}_{gambar.name}"
#             gambar.name = unique_name

#         # Buat instance Berita
#         berita = Berita(author=restaurant_owner, judul=judul, gambar=gambar, konten=konten)
#         berita.save()

#         return HttpResponse(b'CREATED', status=201)
#     except RestaurantOwner.DoesNotExist:
#         return HttpResponse("User is not a Restaurant Owner.", status=403)
#     except Exception as e:
#         return HttpResponse(f"Error: {str(e)}", status=500)

# @login_required()
# def like_berita(request, berita_id):

#     if request.method == "POST":
#         berita = get_object_or_404(Berita, pk=berita_id)
#         status_liked = request.user in berita.like.all()

#         if status_liked: # O(n), is this ok?
#             berita.like.remove(request.user)
#         else:
#             berita.like.add(request.user)
#         return JsonResponse({"likes": berita.like_count, "liked": (not status_liked)})
#     return HttpResponseForbidden()

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
    print(is_restaurant_owner)
    return render(request, "main_berita.html", {'status_user': is_restaurant_owner})

@resto_owner_only(redirect_url="/")
def owner_panel(request):
    return render(request, "owner_panel.html", {'nama': request.user.username, 'id': request.user.id})

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
            for berita in Berita.objects.filter(author_id=request.user.id)
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
