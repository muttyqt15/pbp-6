
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OwnerProfile, CustomerProfile
from api.authentication.models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_resto_owner:
            OwnerProfile.objects.create(user=instance.resto_owner)
        else:
            CustomerProfile.objects.create(user=instance.customer)