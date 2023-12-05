from django.db import models
from users.models import CustomUser
from model_utils import Choices
from users.models import Profile, CustomUser
from datetime import datetime
from datetime import timedelta


class Lesson(models.Model):
    SUBJECTS = Choices(
        (1, "math", "Matematyka"),
        (2, "physics", "Fizyka"),
        (3, "english", "Język angielski"),
    )
    STATUS_CHOICES = Choices(
        (1, "PLANNED", "Planned"),
        (2, "COMPLETED", "Completed"),
        (3, "CANCELLED", "Cancelled"),
    )
    title = models.CharField(max_length=200)
    description = models.CharField(blank=True)
    duration = models.IntegerField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(editable=False)
    tutor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="tutor_lessons"
    )
    student = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="student_lessons"
    )
    subject = models.IntegerField(choices=SUBJECTS)
    status = models.IntegerField(choices=STATUS_CHOICES)
    calendar_meet_link = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.title} || {self.tutor.first_name} {self.tutor.last_name}"

    def save(self, *args, **kwargs):
        if self.start_time and self.duration:
            start_datetime = datetime.combine(self.date, self.start_time)
            self.end_time = (start_datetime + timedelta(minutes=self.duration)).time()

        super(Lesson, self).save(*args, **kwargs)

    # property end_time


class PriceList(models.Model):
    SUBJECTS = Choices(
        (1, "math", "Matematyka"),
        (2, "physics", "Fizyka"),
        (3, "english", "Język angielski"),
    )
    tutor = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="pricelist_set"
    )
    subject = models.IntegerField(choices=SUBJECTS)
    hour_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.tutor.user.email} - {self.get_subject_display()} - {self.hour_price} PLN"

    class Meta:
        unique_together = ("tutor", "subject")
