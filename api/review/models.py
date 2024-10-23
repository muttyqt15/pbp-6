from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid 

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    judul_ulasan = models.CharField(max_length=255)
    penilaian = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    teks_ulasan = models.TextField()
    gambar = models.ImageField(upload_to='images/reviews/', blank=True, null=True)
    tanggal = models.DateField(auto_now_add=True)
    waktu_edit_terakhir = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='review_likes', blank=True)

    def __str__(self):
        return self.judul_ulasan
    
    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def formatted_date(self):
        return self.tanggal.strftime('%d %B %Y')