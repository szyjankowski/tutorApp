from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(null=False, unique=True)
    password = models.CharField()
    #dodac reszte


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class StudentProfile(UserProfile):
    grade = models.CharField(max_length=255, null=True, blank=True)
