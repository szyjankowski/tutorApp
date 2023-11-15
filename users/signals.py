from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import StudentProfile, CustomUser
from tutors.models import TutorProfile


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_tutor:
            TutorProfile.objects.create(user=instance)
        else:
            StudentProfile.objects.create(user=instance)
