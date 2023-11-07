from django.db import models
from users.models import CustomUser
from model_utils import Choices


class PriceList(models.Model):
    SUBJECTS = [
        (1, "Matematyka"),
        (2, "Fizyka"),
        (3, "Język angielski"),
    ]
    subject = models.IntegerField(choices=SUBJECTS)
    hour_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        subject_dict = dict(self.SUBJECTS)
        subject_name = subject_dict.get(self.subject, "Unknown Subject")
        tutor_profile = getattr(self, "tutorprofile", None)
        tutor_email = tutor_profile.user.email if tutor_profile else "No Tutor"
        return f"{tutor_email} - {subject_name} - {self.hour_price} PLN"


class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TutorProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="tutorprofile"
    )
    profile_picture = models.ImageField(
        upload_to="profile_pics/", null=True, blank=True
    )
    description_tutor = models.TextField(blank=True)
    subjects = models.ManyToManyField(Subject, related_name="tutors")  # annotate
    price_list = models.OneToOneField(PriceList, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
