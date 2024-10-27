from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Bookmark
from api.restaurant.models import Restaurant

@login_required
def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('restaurant')
    context = {
        'bookmarks': bookmarks
    }
    return render(request, 'bookmark_list.html', context)

@login_required
@csrf_exempt
def toggle_bookmark(request, restaurant_id):
    if request.method == 'POST':
        print(restaurant_id)
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            restaurant=restaurant
        )
        
        if not created:
            bookmark.delete()
            return JsonResponse({'status': 'removed', "is_favorited": False, "message": "Berhasil!"})
        
        return JsonResponse({'status': 'added', "is_favorited": True, "message": "Berhasil!"})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def delete_bookmark(request, bookmark_id):
    bookmark = get_object_or_404(Bookmark, pk=bookmark_id, user=request.user)
    bookmark.delete()
    return redirect('bookmark:bookmark_list')

