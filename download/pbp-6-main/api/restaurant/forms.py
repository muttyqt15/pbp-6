from django import forms
from .models import Restaurant, Food, Menu

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ["name", "district", "address", "operational_hours", "photo_url"]

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ["category"]
class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ["name", "price"]
