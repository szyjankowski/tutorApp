from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser, Profile
from wallet.models import Wallet


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Wallet.objects.create(user=instance)
