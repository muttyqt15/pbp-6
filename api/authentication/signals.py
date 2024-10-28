from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Customer, RestaurantOwner
from api.user_profile.models import CustomerProfile, OwnerProfile  # Pastikan path ini sesuai

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Buat profil untuk Customer
        if instance.role == "CUSTOMER":
            customer = Customer.objects.create(user=instance)
            CustomerProfile.objects.create(user=customer, bio="", profile_pic=None)
        
        # Buat profil untuk RestaurantOwner
        elif instance.role == "RESTO_OWNER":
            restaurant_owner = RestaurantOwner.objects.create(user=instance)
            OwnerProfile.objects.create(user=restaurant_owner, bio="", profile_pic=None)
