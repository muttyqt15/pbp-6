from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, Food
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
import os
import logging
# Create your views here.

def index(request):
    render(request, 'login.html')


logger = logging.getLogger(__name__)

@login_required
@require_http_methods(["GET", "POST"])
def add_restaurant(request):
    """View to add a new restaurant to the database, with security measures."""

    # Redirect user if they already have a restaurant
    if request.user.is_authenticated and Restaurant.objects.filter(restaurantowner=request.user.restaurantowner).exists():
        restaurant = Restaurant.objects.get(restaurantowner=request.user.restaurantowner)
        return redirect('restaurant', id=restaurant.id)

    form = RestaurantForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        # Strip potentially malicious tags from input fields
        cleaned_name = strip_tags(form.cleaned_data['name'])
        cleaned_district = strip_tags(form.cleaned_data['district'])
        cleaned_address = strip_tags(form.cleaned_data['address'])
        cleaned_operational_hours = strip_tags(form.cleaned_data['operational_hours'])
        photo = form.cleaned_data['photo']

        # Verify the uploaded file is an image
        if isinstance(photo, InMemoryUploadedFile) and not photo.content_type.startswith('image/'):
            logger.warning(f"User {request.user} attempted to upload a non-image file.")
            form.add_error('photo', "Uploaded file must be an image.")
        else:
            # Save the uploaded file and generate a URL
            path = default_storage.save(f'restaurant_photos/{photo.name}', ContentFile(photo.read()))
            photo_url = os.path.join(settings.MEDIA_URL, path)

            # Generate a unique ID for the restaurant
            import uuid
            restaurant_id = uuid.uuid4().int >> 64

            # Create and save the restaurant instance
            restaurant = Restaurant(
                id=restaurant_id,
                restaurantowner=request.user.restaurantowner,
                name=cleaned_name,
                district=cleaned_district,
                address=cleaned_address,
                operational_hours=cleaned_operational_hours,
                photo_url=photo_url
            )
            restaurant.save()

            # Redirect to the newly created restaurant page
            print('success')
            return redirect('restaurant', id=restaurant.id)

    # If the form is not valid, or the request method is GET, render the form
    print('failed')
    return render(request, 'add_restaurant.html', {'form': form})


@resto_owner_only(redirect_url="/login/")
@require_http_methods(["GET", "POST"])
def edit_restaurant(request, id):
    """Edits an existing restaurant in the database"""
    restaurant = get_object_or_404(Restaurant, id=id)
    if request.method == "POST":  # POST request
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            restaurant = form.save(commit=False)  # Save the form data to the database
            restaurant.name = strip_tags(restaurant.name)
            restaurant.district = strip_tags(restaurant.district)
            restaurant.address = strip_tags(restaurant.address)
            restaurant.operational_hours = strip_tags(restaurant.operational_hours)
            restaurant.photo_url = strip_tags(restaurant.photo_url)
            restaurant.save()
            return render(
                request, "edit_restaurant.html", {"form": form, "success": True}
            )  # placeholder

    else:
        form = RestaurantForm(instance=restaurant)
    
    
    return render(request, "edit_restaurant.html", {"form": form})  # placeholder
        

def restaurant(request, id):
    """Main restaurant page"""
    user = request.user
    restaurant = get_object_or_404(Restaurant, id=id)
    food = []  
    categories = set()

    if request.user.is_authenticated:
        if user.is_resto_owner:
            try:
                restaurant = Restaurant.objects.get(restaurantowner=request.user.restaurantowner)
                food = Food.objects.filter(restaurant=restaurant)
                categories = set([f.category for f in food])
            except Restaurant.DoesNotExist:
                restaurant = None
            return render(request, "restaurant.html", {"user": user, "restaurant": restaurant, "foods": food, "categories": categories})
        restaurant = get_object_or_404(Restaurant, id=id)
        food = Food.objects.filter(restaurant=restaurant)
        categories = set([f.category for f in food])     
        
    return render(request, "restaurant.html", {"user": user, "restaurant": restaurant, "foods": food, "categories": categories})
    
        



def get_restaurant_menu(request, id):
    """Returns a single restaurant's menu by ID"""
    restaurant = get_object_or_404(Restaurant, id=id)
    food = Food.objects.filter(restaurant=restaurant)
    return render(request, "restaurant_menu.html", {"restaurant": restaurant, "food": food})

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

