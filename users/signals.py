from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from tutors.models import Profile


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_tutor:
            Profile.objects.create(user=instance)
        else:
            Profile.objects.create(user=instance)
