from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'restoran', 'judul_ulasan', 'penilaian', 'tanggal', 'waktu_edit_terakhir', 'total_likes')
    search_fields = ('customer__user__username', 'restoran__name', 'judul_ulasan', 'teks_ulasan')
    list_filter = ('penilaian', 'tanggal', 'restoran')
    readonly_fields = ('id', 'tanggal', 'waktu_edit_terakhir', 'total_likes')
    
    # Function to display total likes in the admin panel
    def total_likes(self, obj):
        return obj.total_likes
    total_likes.short_description = 'Total Likes'

admin.site.register(Review, ReviewAdmin)
