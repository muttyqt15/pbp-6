from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, Food, Menu
from .forms import RestaurantForm, FoodForm
from django.utils.html import strip_tags
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.decorators.http import require_http_methods, require_POST
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.decorators import login_required
from api.authentication.decorators import resto_owner_only
from django.utils.html import strip_tags
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os, json
from api.authentication.models import User, RestaurantOwner, Customer
import logging
from django.db.models import Q
from api.bookmark.models import Bookmark
logger = logging.getLogger(__name__)


@resto_owner_only(redirect_url="/auth/login/")
@require_http_methods(["GET", "POST"])
def add_restaurant(request):
    """View to add a new restaurant to the database, with security measures."""

    # Redirect user if they already have a restaurant
    if Restaurant.objects.filter(restaurantowner=request.user.resto_owner).exists():
        restaurant = Restaurant.objects.get(
            restaurantowner=request.user.resto_owner
        )
        return redirect("restaurant", id=restaurant.id)

    form = RestaurantForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            # Strip potentially malicious tags from input fields
            cleaned_name = strip_tags(form.cleaned_data["name"])
            cleaned_district = strip_tags(form.cleaned_data["district"])
            cleaned_address = strip_tags(form.cleaned_data["address"])
            cleaned_operational_hours = strip_tags(form.cleaned_data["operational_hours"])
            photo = form.cleaned_data.get("photo")

            # Verify the uploaded file is an image
            if photo:
                if isinstance(photo, InMemoryUploadedFile) and not photo.content_type.startswith("image/"):
                    form.add_error("photo", "Uploaded file must be an image.")
                else:
                    # Save the uploaded file and generate a URL
                    path = default_storage.save(f"restaurant_photos/{photo.name}", ContentFile(photo.read()))
                    photo_url = os.path.join(settings.MEDIA_URL, path)

                    # Create and save the restaurant instance
                    restaurant = Restaurant(
                        name=cleaned_name,
                        district=cleaned_district,
                        address=cleaned_address,
                        operational_hours=cleaned_operational_hours,
                        photo_url=photo_url,
                    )
                    restaurant.save()

                    # Link the restaurant to the restaurant owner
                    restaurant_owner = request.user.resto_owner
                    restaurant_owner.restaurant = restaurant
                    restaurant_owner.save()

                    # Redirect to the newly created restaurant page
                    return redirect("restaurant", id=restaurant.id)

            else:
                # Create and save the restaurant instance without a photo
                restaurant = Restaurant(
                    name=cleaned_name,
                    district=cleaned_district,
                    address=cleaned_address,
                    operational_hours=cleaned_operational_hours,
                )
                restaurant.save()

                # Link the restaurant to the restaurant owner
                restaurant_owner = request.user.resto_owner
                restaurant_owner.restaurant = restaurant
                restaurant_owner.save()

                # Redirect to the newly created restaurant page
                return redirect("restaurant", id=restaurant.id)

    # If the form is not valid, or the request method is GET, render the form
    return render(request, "add_restaurant.html", {"form": form})


@login_required
@resto_owner_only(redirect_url="/auth/login/")
@require_http_methods(["POST"])
def edit_restaurant(request, id):
    """
    View to edit an existing restaurant using AJAX.
    Only the owner of the restaurant can edit it.
    """
    restaurant = get_object_or_404(Restaurant, id=id, restaurantowner=request.user.resto_owner)

    try:
        # Parse the incoming JSON data
        data = json.loads(request.body)
        field_name = data.get('field')
        value = strip_tags(data.get('value'))

        # Update the appropriate field based on the field_name
        if field_name in ['name', 'district', 'address', 'operational_hours']:
            setattr(restaurant, field_name, value)
            restaurant.save()
            return JsonResponse({'success': True, 'message': 'Field updated successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid field name.'})

    except Exception as e:
        logger.error(f"Error updating restaurant: {e}")
        return JsonResponse({'success': False, 'message': 'Failed to update restaurant due to an unexpected error.'})

def restaurant_list(request):
    """View to list all restaurants."""
    restaurants = Restaurant.objects.all()
    return render(request, "all_restaurants.html", {"restaurants": restaurants})


def restaurant(request, id):
    """Main restaurant page"""
    user = request.user
    restaurant = get_object_or_404(Restaurant, id=id)
    food = []
    categories = set()
    reviews = restaurant.reviews.all()

    # More detailed debug prints
    print(f"User authenticated: {request.user.is_authenticated}")
    if request.user.is_authenticated:
        print(f"Username: {user.username}")
        print(f"Is resto owner: {user.is_resto_owner}")
        if hasattr(user, "resto_owner"):
            print(f"Has resto_owner profile: Yes")
            print(f"resto_owner instance: {user.resto_owner}")
            print(f"resto_owner restaurant: {user.resto_owner.restaurant}")
            if user.resto_owner.restaurant:
                print(f"Owner restaurant ID: {user.resto_owner.restaurant.id}")
            else:
                print("Owner restaurant: None")
        else:
            print("Has resto_owner profile: No")
        print(f"Viewing restaurant ID: {restaurant.id}")

    if request.user.is_authenticated:
        if user.is_resto_owner:
            is_owner = (
                hasattr(user, "resto_owner")
                and user.resto_owner.restaurant is not None
                and user.resto_owner.restaurant.id == restaurant.id
            )

            print(f"Is owner check result: {is_owner}")

            menus = Menu.objects.filter(restaurant=restaurant)

            categories = set([f.category for f in menus])
            is_favorited = Bookmark.objects.filter(user=request.user).exists()
            return render(
                request,
                "restaurant.html",
                {
                    "user": user,
                    "restaurant": restaurant,
                    "foods": food,
                    "categories": categories,
                    "is_owner": is_owner,
                    "is_favorited": is_favorited,
                    "reviews": reviews,
                },
            )

        menus = Menu.objects.filter(restaurant=restaurant)

        categories = set([f.category for f in menus])

    return render(
        request,
        "restaurant.html",
        {
            "user": user,
            "restaurant": restaurant,
            "foods": food,
            "categories": categories,
            "is_owner": False,
            "reviews": reviews,
        },
    )


@resto_owner_only(redirect_url="/login/")
@require_http_methods(["POST"])
def add_menu(request):
    """
    View to add a new menu to a restaurant using AJAX.
    Only the owner of the restaurant can add a menu.
    """
    try:
        data = json.loads(request.body)
        menu_category = strip_tags(data.get('category', '').strip())

        # Ensure the category name is valid
        if not menu_category:
            return JsonResponse({'success': False, 'message': 'Menu category is required.'})

        # Ensure the user is a restaurant owner and has a restaurant
        if not hasattr(request.user, 'resto_owner') or not request.user.resto_owner.restaurant:
            return JsonResponse({'success': False, 'message': 'You do not have permission to add a menu.'})

        restaurant = request.user.resto_owner.restaurant

        # Create and save the new menu
        menu = Menu(category=menu_category, restaurant=restaurant)
        menu.save()

        return JsonResponse({'success': True, 'message': 'Menu added successfully.'})
    except Exception as e:
        logger.error(f"Error adding menu: {e}")
        return JsonResponse({'success': False, 'message': 'Failed to add menu due to an unexpected error.'})


@resto_owner_only(redirect_url="/login/")
@require_http_methods(["POST"])
def delete_menu(request):
    """
    View to handle deleting a menu using AJAX.
    Only the owner of the restaurant can delete menus.
    """
    try:
        data = json.loads(request.body)
        menu_id = data.get('menu_id')

        # Ensure the user is a restaurant owner and has a restaurant
        if not request.user.is_resto_owner:
            return JsonResponse({'success': False, 'message': 'You do not have permission to delete this menu.'})

        # Get the menu to delete
        try:
            menu = Menu.objects.get(id=menu_id, restaurant=request.user.resto_owner.restaurant)
        except Menu.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Menu does not exist or you do not have permission.'})

        # Delete the menu
        menu.delete()

        return JsonResponse({'success': True, 'message': 'Menu deleted successfully.'})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data.'})

    except Exception as e:
        logger.error(f"Error deleting menu: {e}")
        return JsonResponse({'success': False, 'message': 'Failed to delete menu due to an unexpected error.'})
    

@resto_owner_only(redirect_url="/login/")
@require_http_methods(["POST"])
def add_food(request):
    """
    View to add a new food item to a menu using AJAX.
    Only the owner of the restaurant can add food items.
    """
    try:
        data = json.loads(request.body)
        food_name = strip_tags(data.get('name', '').strip())
        food_price = strip_tags(data.get('price', '').strip())
        menu_id = data.get('menu_id')

        # Ensure the food name and price are valid
        if not food_name or not food_price:
            return JsonResponse({'success': False, 'message': 'Food name and price are required.'})

        # Ensure the user is a restaurant owner and has a restaurant
        if not request.user.is_resto_owner:
            return JsonResponse({'success': False, 'message': 'You do not have permission to add a food item.'})

        # Get the menu to which the food item will be added
        try:
            menu = Menu.objects.get(id=menu_id, restaurant=request.user.resto_owner.restaurant)
        except Menu.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Menu does not exist or you do not have permission.'})

        # Create and save the new food item (ID will be automatically generated)
        food = Food(name=food_name, price=food_price, menu=menu)
        food.save()

        return JsonResponse({'success': True, 'message': 'Food item added successfully.'})
    
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data.'})
    
    except Exception as e:
        logger.error(f"Error adding food item: {e}")
        return JsonResponse({'success': False, 'message': 'Failed to add food item due to an unexpected error.'})

@resto_owner_only(redirect_url="/login/")
@require_http_methods(["POST"])
def update_photo(request):
    """
    View to handle updating a restaurant's photo using AJAX.
    Only the owner of the restaurant can update the photo.
    """
    try:
        # Ensure the user is a restaurant owner and has a restaurant
        if not request.user.is_resto_owner:
            return JsonResponse({'success': False, 'message': 'You do not have permission to update this photo.'})

        # Get the restaurant associated with the user
        try:
            restaurant = request.user.resto_owner.restaurant
        except Restaurant.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Restaurant does not exist or you do not have permission.'})

        # Get the uploaded photo file
        photo = request.FILES.get('photo')
        if not photo:
            return JsonResponse({'success': False, 'message': 'No photo provided.'})

        # Check if the uploaded file is an image
        if isinstance(photo, InMemoryUploadedFile) and not photo.content_type.startswith("image/"):
            return JsonResponse({'success': False, 'message': 'Uploaded file must be an image.'})

        # Save the uploaded file and generate a URL
        path = default_storage.save(f"restaurant_photos/{photo.name}", ContentFile(photo.read()))
        photo_url = os.path.join(settings.MEDIA_URL, path)

        # Update the restaurant instance with the new photo URL
        restaurant.photo_url = photo_url
        restaurant.save()

        return JsonResponse({'success': True, 'message': 'Photo updated successfully.'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to update photo due to an unexpected error: {str(e)}'})    


@resto_owner_only(redirect_url="/login/")
@require_http_methods(["POST"])
def edit_menu_category(request):
    """
    View to handle editing a menu category using AJAX.
    Only the owner of the restaurant can edit menu categories.
    """
    try:
        data = json.loads(request.body)
        category_id = data.get('category_id')
        new_category_name = data.get('category_name', '').strip()

        # Ensure the user is a restaurant owner and has a restaurant
        if not request.user.is_resto_owner:
            return JsonResponse({'success': False, 'message': 'You do not have permission to edit this menu category.'})

        # Get the menu category to edit
        try:
            menu = Menu.objects.get(id=category_id, restaurant=request.user.resto_owner.restaurant)
        except Menu.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Menu category does not exist or you do not have permission.'})

        # Update the menu category
        if new_category_name:
            menu.category = new_category_name
            menu.save()

        return JsonResponse({'success': True, 'message': 'Menu category updated successfully.'})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data.'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to update menu category due to an unexpected error: {str(e)}'})

@resto_owner_only(redirect_url="/login/")
@require_http_methods(["POST"])
def edit_food(request):
    """
    View to handle editing a food item using AJAX.
    Only the owner of the restaurant can edit food items.
    """
    try:
        data = json.loads(request.body)
        food_id = data.get('food_id')
        new_food_name = data.get('food_name', '').strip()
        new_food_price = data.get('food_price', '').strip()

        # Ensure the user is a restaurant owner and has a restaurant
        if not request.user.is_resto_owner:
            return JsonResponse({'success': False, 'message': 'You do not have permission to edit this food item.'})

        # Get the food item to edit
        try:
            food = Food.objects.get(id=food_id, menu__restaurant=request.user.resto_owner.restaurant)
        except Food.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Food item does not exist or you do not have permission.'})

        # Update the food item
        if new_food_name and new_food_price:
            food.name = new_food_name
            food.price = new_food_price
            food.save()

        return JsonResponse({'success': True, 'message': 'Food item updated successfully.'})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data.'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to update food item due to an unexpected error: {str(e)}'})

@resto_owner_only(redirect_url="/login/")
@require_http_methods(["POST"])
def delete_food(request):
    """
    View to handle deleting a food item using AJAX.
    Only the owner of the restaurant can delete food items.
    """
    try:
        data = json.loads(request.body)
        food_id = data.get('food_id')

        # Ensure the user is a restaurant owner and has a restaurant
        if not request.user.is_resto_owner:
            return JsonResponse({'success': False, 'message': 'You do not have permission to delete this food item.'})

        # Get the food item to delete
        try:
            food = Food.objects.get(id=food_id, menu__restaurant=request.user.resto_owner.restaurant)
        except Food.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Food item does not exist or you do not have permission.'})

        # Delete the food item
        food.delete()

        return JsonResponse({'success': True, 'message': 'Food item deleted successfully.'})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data.'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to delete food item due to an unexpected error: {str(e)}'})
    
require_POST
def filter_restaurants(request):
    """Handles AJAX requests to filter and sort restaurants."""
    import json

    # Get data from request
    try:
        data = json.loads(request.body)
        search_query = data.get('search', '').lower()
        sort_by = data.get('sort_by', '')

        # Filter restaurants by search query
        restaurants = Restaurant.objects.all()
        if search_query:
            restaurants = restaurants.filter(
                Q(name__icontains=search_query) | Q(district__icontains=search_query)
            )

        # Sort restaurants based on the selected criteria
        if sort_by:
            restaurants = restaurants.order_by(sort_by)

        # Serialize restaurants to JSON format
        restaurant_list = []
        for restaurant in restaurants:
            restaurant_list.append({
                'id': restaurant.id,
                'name': restaurant.name,
                'district': restaurant.district,
                'address': restaurant.address,
                'operational_hours': restaurant.operational_hours,
                'photo_url': restaurant.photo_url,
            })

        return JsonResponse({'restaurants': restaurant_list}, safe=False)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    

def menu_view(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    menus = restaurant.menu.all()  # Get all menus for the restaurant
    return render(request, 'menu_card.html', {'menus': menus})

def get_restaurant_menu(request, id):
    """Returns a single restaurant's menu by ID"""
    restaurant = get_object_or_404(Restaurant, id=id)
    food = Food.objects.filter(menu__restaurant=restaurant)

    return render(
        request, "restaurant_menu.html", {"restaurant": restaurant, "food": food}
    )


def get_restaurant_xml(request):
    """Returns a list of all restaurants in XML format"""
    restaurants = Restaurant.objects.all()
    data = serializers.serialize("xml", restaurants)
    return HttpResponse(data, content_type="application/xml")


def get_restaurants_xml_by_id(request, id):
    """Returns a list of select restaurants in XML format (by ID)"""
    restaurants = Restaurant.objects.filter(id=id)
    data = serializers.serialize("xml", restaurants)
    return HttpResponse(data, content_type="application/xml")


def get_restaurants_json(request):
    """Returns a list of all restaurants in JSON format"""
    restaurants = Restaurant.objects.all()
    data = serializers.serialize("json", restaurants)
    return JsonResponse(data, safe=False)


def get_restaurants_json_by_id(request, id):
    """Returns a list of select restaurants in JSON format (by ID)"""
    restaurants = Restaurant.objects.filter(id=id)
    data = serializers.serialize("json", restaurants)
    return JsonResponse(data, safe=False)
