# from django.contrib import admin

# # Register your models here.
# from django.contrib import admin
# from .models import Review

# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ('customer', 'restoran', 'judul_ulasan', 'penilaian', 'tanggal', 'waktu_edit_terakhir', 'total_likes')
#     search_fields = ('customer__user__username', 'restoran__name', 'judul_ulasan', 'teks_ulasan')
#     list_filter = ('penilaian', 'tanggal', 'restoran')
#     readonly_fields = ('id', 'tanggal', 'waktu_edit_terakhir', 'total_likes')
    
#     # Function to display total likes in the admin panel
#     def total_likes(self, obj):
#         return obj.total_likes
#     total_likes.short_description = 'Total Likes'

# admin.site.register(Review, ReviewAdmin)

from django.contrib import admin
from .models import Review, ReviewImage

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'restoran', 'judul_ulasan', 'penilaian', 'tanggal', 'waktu_edit_terakhir', 'display_total_likes')
    search_fields = ('customer__user__username', 'restoran__name', 'judul_ulasan', 'teks_ulasan')
    list_filter = ('penilaian', 'tanggal', 'restoran')
    readonly_fields = ('id', 'tanggal', 'waktu_edit_terakhir', 'display_total_likes')

    def display_total_likes(self, obj):
        return obj.total_likes
    display_total_likes.short_description = 'Total Likes'

@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ('review', 'image')
    search_fields = ('review__judul_ulasan',)
    readonly_fields = ('id',)

