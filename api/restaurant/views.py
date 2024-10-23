from django.shortcuts import render, get_object_or_404
from .models import Restaurant, Food
from .forms import RestaurantForm, FoodForm
from django.utils.html import strip_tags
from django.http import HttpResponse, JsonResponse
from django.core import serializers

# Create your views here.

def index(request):
    render(request, 'login.html')


def add_restaurant(request):
    """Adds a new restaurant to the database"""
    if request.method == "POST":  # POST request
        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)  # Save the form data to the database
            restaurant.name = strip_tags(restaurant.name)
            restaurant.district = strip_tags(restaurant.district)
            restaurant.address = strip_tags(restaurant.address)
            restaurant.operational_hours = strip_tags(restaurant.operational_hours)
            restaurant.photo_url = strip_tags(restaurant.photo_url)
            restaurant.save()
            return render(
                request, "add_restaurant.html", {"form": form, "success": True}
            )  # placeholder

    else:
        form = RestaurantForm()
    return render(request, "add_restaurant.html", {"form": form})  # placeholder


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
