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

logger = logging.getLogger(__name__)


@resto_owner_only(redirect_url="/login/")
@require_http_methods(["GET", "POST"])
def add_restaurant(request):
    """View to add a new restaurant to the database, with security measures."""

    # Redirect user if they already have a restaurant
    if Restaurant.objects.filter(restaurantowner=request.user.restaurantowner).exists():
        restaurant = Restaurant.objects.get(
            restaurantowner=request.user.restaurantowner
        )
        return redirect("restaurant", id=restaurant.id)

    form = RestaurantForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        # Strip potentially malicious tags from input fields
        cleaned_name = strip_tags(form.cleaned_data["name"])
        cleaned_district = strip_tags(form.cleaned_data["district"])
        cleaned_address = strip_tags(form.cleaned_data["address"])
        cleaned_operational_hours = strip_tags(form.cleaned_data["operational_hours"])
        photo = form.cleaned_data["photo"]

        # Verify the uploaded file is an image
        if isinstance(
            photo, InMemoryUploadedFile
        ) and not photo.content_type.startswith("image/"):
            logger.warning(f"User {request.user} attempted to upload a non-image file.")
            form.add_error("photo", "Uploaded file must be an image.")
        else:
            # Save the uploaded file and generate a URL
            path = default_storage.save(
                f"restaurant_photos/{photo.name}", ContentFile(photo.read())
            )
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
            restaurant_owner = request.user.restaurantowner
            restaurant_owner.restaurant = restaurant
            restaurant_owner.save()

            # Redirect to the newly created restaurant page
            print("success")
            return redirect("restaurant", id=restaurant.id)

    # If the form is not valid, or the request method is GET, render the form
    print("failed")
    return render(request, "add_restaurant.html", {"form": form})


@login_required
@resto_owner_only(redirect_url="/login/")
@require_http_methods(["POST"])
def edit_restaurant(request, id):
    """
    View to edit an existing restaurant using AJAX.
    Only the owner of the restaurant can edit it.
    """
    restaurant = get_object_or_404(Restaurant, id=id, restaurantowner=request.user.restaurantowner)

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


def restaurant(request, id):
    """Main restaurant page"""
    user = request.user
    restaurant = get_object_or_404(Restaurant, id=id)
    food = []
    categories = set()

    # More detailed debug prints
    print(f"User authenticated: {request.user.is_authenticated}")
    if request.user.is_authenticated:
        print(f"Username: {user.username}")
        print(f"Is resto owner: {user.is_resto_owner}")
        if hasattr(user, "restaurantowner"):
            print(f"Has RestaurantOwner profile: Yes")
            print(f"RestaurantOwner instance: {user.restaurantowner}")
            print(f"RestaurantOwner restaurant: {user.restaurantowner.restaurant}")
            if user.restaurantowner.restaurant:
                print(f"Owner restaurant ID: {user.restaurantowner.restaurant.id}")
            else:
                print("Owner restaurant: None")
        else:
            print("Has RestaurantOwner profile: No")
        print(f"Viewing restaurant ID: {restaurant.id}")

    if request.user.is_authenticated:
        if user.is_resto_owner:
            is_owner = (
                hasattr(user, "restaurantowner")
                and user.restaurantowner.restaurant is not None
                and user.restaurantowner.restaurant.id == restaurant.id
            )

            print(f"Is owner check result: {is_owner}")

            food = Food.objects.filter(menu__restaurant=restaurant)

            categories = set([f.category for f in food])

            return render(
                request,
                "restaurant.html",
                {
                    "user": user,
                    "restaurant": restaurant,
                    "foods": food,
                    "categories": categories,
                    "is_owner": is_owner,
                },
            )

        food = Food.objects.filter(menu__restaurant=restaurant)

        categories = set([f.category for f in food])

    return render(
        request,
        "restaurant.html",
        {
            "user": user,
            "restaurant": restaurant,
            "foods": food,
            "categories": categories,
            "is_owner": False,
        },
    )


@login_required
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
        if not hasattr(request.user, 'restaurantowner') or not request.user.restaurantowner.restaurant:
            return JsonResponse({'success': False, 'message': 'You do not have permission to add a menu.'})

        restaurant = request.user.restaurantowner.restaurant

        # Create and save the new menu
        menu = Menu(category=menu_category, restaurant=restaurant)
        menu.save()

        return JsonResponse({'success': True, 'message': 'Menu added successfully.'})
    except Exception as e:
        logger.error(f"Error adding menu: {e}")
        return JsonResponse({'success': False, 'message': 'Failed to add menu due to an unexpected error.'})


@login_required
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
            menu = Menu.objects.get(id=menu_id, restaurant=request.user.restaurantowner.restaurant)
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
