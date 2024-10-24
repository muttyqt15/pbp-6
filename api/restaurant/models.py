from django.db import models


class Restaurant(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    address = models.TextField()
    operational_hours = models.CharField(max_length=255)
    photo_url = models.URLField()
    def __str__(self):
        return self.name


class Food(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menu_items"
    )
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.CharField(max_length=255)

    def __str__(self): 
        return f"{self.name} at {self.restaurant.name}"
