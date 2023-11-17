from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy

from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    email = models.EmailField(gettext_lazy("email adress"), unique=True)
    first_name = models.TextField()
    last_name = models.TextField()
    is_tutor = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class StudentProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="studentprofile"
    )
    profile_picture = models.ImageField(
        upload_to="profile_pics/", null=True, blank=True
    )
    description_student = models.TextField(blank=True)

    def __str__(self):
        return self.user.email
