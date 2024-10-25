from django.db import models
from api.authentication.models import RestaurantOwner
from api.authentication.models import User
import uuid

class Berita(models.Model):
    author = models.ForeignKey(RestaurantOwner, on_delete=models.CASCADE, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    judul = models.CharField(max_length=255)
    gambar = models.ImageField(upload_to='images/', blank=True, null=True)  
    konten = models.TextField()
    jumlah_like = models.ManyToManyField(User)
    tanggal = models.DateTimeField(auto_now_add=True)
    tanggal_pembaruan = models.DateTimeField(auto_now=True)

    @property
    def like_count(self):
        return self.jumlah_like.count()

