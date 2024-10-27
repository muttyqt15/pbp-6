
from django.db import models
from django.contrib.auth.models import User
from restaurant.models import Restaurant

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)  # Optional notes for the bookmark

    class Meta:
        unique_together = ('user', 'restaurant')  # Prevent duplicate bookmarks

    def str(self):
        return f"{self.user.username} - {self.restaurant.name}"