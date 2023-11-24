from django.db import models
from users.models import CustomUser
from model_utils import Choices


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profile"
    )
    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        null=True,
        blank=True,
        default="profile_pics/user_pfp.png",
    )
    description = models.TextField(blank=True)

    @property
    def price_lists(self):
        return self.pricelist_set.all()

    def __str__(self):
        return self.user.email


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
        subject_dict = self.SUBJECTS._identifier_map
        subject_name = subject_dict.get(self.subject, "Unknown Subject")
        return f"{self.tutor.user.email} - {subject_name} - {self.hour_price} PLN"

    class Meta:
        unique_together = ("tutor", "subject")
