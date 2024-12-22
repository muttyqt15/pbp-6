from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Bookmark
from api.restaurant.models import Restaurant
from django.views.decorators.http import require_http_methods

@login_required
def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('restaurant')
    context = {
        'bookmarks': bookmarks
    }
    return render(request, 'bookmark_list.html', context)

# @login_required
# @csrf_exempt
# def toggle_bookmark(request, restaurant_id):
#     if request.method == 'POST':
#         print(restaurant_id)
#         restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
#         bookmark, created = Bookmark.objects.get_or_create(
#             user=request.user,
#             restaurant=restaurant
#         )
        
#         if not created:
#             bookmark.delete()
#             return JsonResponse({'status': 'removed', "is_favorited": False, "message": "Berhasil!"})
        
#         return JsonResponse({'status': 'added', "is_favorited": True, "message": "Berhasil!"})
    
#     return JsonResponse({'error': 'Invalid request'}, status=400)
@login_required
@csrf_exempt
def toggle_bookmark(request, restaurant_id):
    if request.method == 'POST':
        try:
            # Fetch the restaurant or return 404 if not found
            restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

            # Toggle the bookmark
            bookmark, created = Bookmark.objects.get_or_create(
                user=request.user,
                restaurant=restaurant
            )

            if not created:
                bookmark.delete()
                return JsonResponse({'status': 'removed', "is_favorited": False, "message": "Bookmark removed successfully!"})
            
            return JsonResponse({'status': 'added', "is_favorited": True, "message": "Bookmark added successfully!"})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
@require_http_methods(["POST", "DELETE"])
@login_required
def delete_bookmark(request, bookmark_id):
    try:
        # Ensure the bookmark exists and belongs to the logged-in user
        bookmark = get_object_or_404(Bookmark, restaurant__id=bookmark_id, user=request.user)
        bookmark.delete()
        return JsonResponse({'status': 'success', 'message': 'Bookmark removed successfully.'}, status=200)

    except Bookmark.DoesNotExist:
        return JsonResponse(
            {'status': 'error', 'message': 'Bookmark not found or does not belong to the user.'},
            status=404
        )

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Failed to remove bookmark: {str(e)}'}, status=500)



@login_required
def get_bookmarks(request):
    # Query all bookmarks for the logged-in user
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('restaurant')

    # Build the JSON response
    data = [
        {
            'id': bookmark.restaurant.id,
            'name': bookmark.restaurant.name,
            'address': bookmark.restaurant.address,
            'is_favorited': True  # Always true for bookmarks
        }
        for bookmark in bookmarks
    ]

    return JsonResponse({'bookmarks': data}, safe=False)



# @login_required
# @csrf_exempt
# def delete_bookmark(request, bookmark_id):
#     bookmark = get_object_or_404(Bookmark, pk=bookmark_id, user=request.user)
#     bookmark.delete()
#     return redirect('bookmark:bookmark_list')

