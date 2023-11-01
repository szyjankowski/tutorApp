from django.db import models
from users.models import CustomUser


class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TutorProfile(models.Model):
    tutor = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="tutorprofile"
    )
    profile_picture = models.ImageField(
        upload_to="profile_pics/", null=True, blank=True
    )
    description_tutor = models.TextField(blank=True)
    subjects = models.ManyToManyField(Subject, related_name="tutors")

    def __str__(self):
        return self.tutor.email


class PriceList(models.Model):
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    hour_price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ("tutor", "subject")

    def __str__(self):
        return f"{self.tutor.tutor.email} - {self.subject.name} - {self.hour_price} PLN"
