from django.contrib import admin
from .models import Berita  # Ganti dengan path yang benar jika perlu

class BeritaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'author', 'tanggal', 'tanggal_pembaruan')  # Menampilkan field ini di daftar admin
    search_fields = ('judul',)  # Menambahkan fungsi pencarian berdasarkan judul

# Mendaftarkan model Berita
admin.site.register(Berita, BeritaAdmin)
