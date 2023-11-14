from django.test import TestCase
from users.models import CustomUser
from tutors.models import TutorProfile

USER_EMAIL = "tutor@example.com"
USER_PASSWORD = "password123"


# Create your tests here.


class TutorProfileModelTest(TestCase):
    def setUp(self):
        # Create a user and a tutor profile
        self.user = CustomUser.objects.create_user(
            email=USER_EMAIL, password=USER_PASSWORD
        )
        self.tutor_profile = TutorProfile.objects.create(user=self.user)

    def test_tutor_profile_creation(self):
        self.assertEqual(self.tutor_profile.user, self.user)

    def test_tutor_profile_string_representation(self):
        self.assertEqual(str(self.tutor_profile), USER_EMAIL)
