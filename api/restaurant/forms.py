from django.forms import ModelForm
from .models import Restaurant, Food

class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ["name", "district", "address", "operational_hours", "photo_url"]


class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ["name", "category", "price"]
