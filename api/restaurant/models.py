from django.db import models


class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    address = models.TextField()
    operational_hours = models.CharField(max_length=255)
    photo_url = models.URLField(blank=True) 
    

    def __str__(self):
        return self.name

class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menu"
    )

    def __str__(self):
        return f"Menu for {self.restaurant.name}"

class Food(models.Model):
    id = models.AutoField(primary_key=True)
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name="food", null=True, blank=True
    )
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    def __str__(self): 
        return f"{self.name} at {self.restaurant.name}"
