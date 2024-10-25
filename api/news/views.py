from django.shortcuts import render, redirect
from django.urls import reverse
from api.news.forms import BeritaEntryForm
from api.news.models import Berita
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core import serializers
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.http import JsonResponse
import os



def show_main(request):
    berita = Berita.objects.all()
    context = {
        'berita_list' : berita
    }
    return render(request, "main_berita.html", context)

def owner_panel(request):
    berita = Berita.objects.all()
    # berita = Berita.objects.filter(author=owner_id)

    context = {
        'berita_list' : berita
    }
    return render(request, "owner_panel.html", context)

def berita_entry(request):
    form = BeritaEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        berita_entry = form.save(commit=False)
        berita_entry.author = request.user
        berita_entry.save()
        return redirect('main:show_main')

    context = {"form": form}
    return render(request, "berita_entry.html", context)

def show_berita_json(request):
    try:
        data = Berita.objects.all()
        if not data:  # Jika data kosong
            return HttpResponse(status=404)
        return HttpResponse(serializers.serialize("json", data), content_type="application/json")
    except Exception as e:
        # Tangani error dan kirimkan respons
        return HttpResponse(f"Error: {str(e)}", status=500)


def show_berita_by_id(request, berita_id):
    try:
        data = Berita.objects.filter(id=berita_id)
        if not data.exists():
            return HttpResponse("Berita with this ID not found", status=404)
        return HttpResponse(serializers.serialize("json", data), content_type="application/json")
    except Exception as e:
        # Menangani error tak terduga dan mengirimkan respons status 500
        return HttpResponse(f"Error: {str(e)}", status=500)


def show_berita_by_owner(request):
    try:
        data = Berita.objects.filter(author=request.user)
        if not data.exists():  # Jika user tidak memiliki berita
            return HttpResponse("You don't have any news entries", status=404)
        return HttpResponse(serializers.serialize("json", data), content_type="application/json")
    except Exception as e:
        # Menangani error tak terduga dan mengirimkan respons status 500
        return HttpResponse(f"Error: {str(e)}", status=500)


# Dalam view pengeditan berita

def edit_berita(request, berita_id):
    try:
        berita = Berita.objects.get(pk=berita_id)
        gambar = berita.gambar
        
        if request.method == 'POST':
            form = BeritaEntryForm(request.POST, request.FILES, instance=berita)

            if form.is_valid():

                if berita.gambar and os.path.isfile(berita.gambar.path):
                    os.remove(berita.gambar.path)
                    
                if 'image' in request.FILES:
                    berita.gambar = request.FILES['image']
                berita.tanggal_pembaruan = timezone.now()
                form.save()

                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Form is not valid'}, status=400)

        # Jika GET request, kembalikan data dalam format JSON untuk diisi ke modal
        berita_data = serializers.serialize('json', [berita])
        return HttpResponse(berita_data, content_type="application/json")

    except Berita.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Berita not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# def edit_berita(request, berita_id):
#     try:
#         berita = Berita.objects.get(pk=berita_id)
        
#         if request.method == 'POST':
#             form = BeritaEntryForm(request.POST, request.FILES, instance=berita)

#             if form.is_valid():
#                 if 'image' in request.FILES:
#                     berita.gambar = request.FILES['image']
#                 berita.tanggal_pembaruan = timezone.now()
#                 form.save()

#                 return JsonResponse({'status': 'success'})
#             else:
#                 return JsonResponse({'status': 'error', 'message': 'Form is not valid'}, status=400)

#         # Jika GET request, kembalikan data dalam format JSON untuk diisi ke modal
#         berita_data = serializers.serialize('json', [berita])
#         return HttpResponse(berita_data, content_type="application/json")

#     except Berita.DoesNotExist:
#         return JsonResponse({'status': 'error', 'message': 'Berita not found'}, status=404)
#     except Exception as e:
#         return JsonResponse({'status': 'error', 'message': str(e)}, status=500)




def delete_berita(request, berita_id):
    try:
        berita = Berita.objects.get(pk=berita_id)
        
        # Hapus image jika ada
        if berita.gambar and os.path.isfile(berita.gambar.path):
            os.remove(berita.gambar.path)

        berita.delete()
        return HttpResponseRedirect(reverse('news:show_main'))
    
    except Berita.DoesNotExist:
        return HttpResponse("Berita not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)


@csrf_exempt
@require_POST
def add_berita_ajax(request):
    try:
        # author = request.user
        judul = strip_tags(request.POST.get("judul"))
        gambar = request.FILES.get("gambar")
        konten = strip_tags(request.POST.get("konten"))

        berita = Berita( judul=judul, gambar=gambar, konten=konten)
        berita.save()

        return HttpResponse(b'CREATED', status=201)
    except Exception as e:
        # Kirim respons error ke frontend
        return HttpResponse(f"Error: {str(e)}", status=500)
