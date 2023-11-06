from django.db import models
from users.models import CustomUser
from model_utils import Choices


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

    def __str__(self):
        return self.user.email


class PriceList(models.Model):
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE)  # wywalic
    subject = Choices((1, "Matematyka"), (2, "Fizyka"))
    hour_price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ("tutor", "subject")

    def __str__(self):
        return f"{self.tutor.user.email} - {self.subject.name} - {self.hour_price} PLN"
