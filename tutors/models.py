from django.db import models
from django.db import models
from users.models import UserProfile


class TutorProfile(UserProfile):
    hourly_rate = models.DecimalField(max_digits=5, decimal_places=2)
