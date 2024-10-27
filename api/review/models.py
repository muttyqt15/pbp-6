from django.db import models
from api.authentication.models import Customer, User
from api.restaurant.models import Restaurant
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    restoran = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews', null=True)
    judul_ulasan = models.CharField(max_length=255)
    tanggal = models.DateField(auto_now_add=True)
    teks_ulasan = models.TextField()
    penilaian = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    waktu_edit_terakhir = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="liked_reviews", blank=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Review by {self.get_display_name} on {self.restoran.name}"

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def get_display_name(self):
        return self.display_name if self.display_name else "Anonymous"

class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="images/reviews/")
