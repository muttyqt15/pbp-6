from django import forms
from .models import Restaurant, Food

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ["name", "district", "address", "operational_hours", "photo_url"]


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ["name", "category", "price"]
