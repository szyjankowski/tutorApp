from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomUser
from model_bakery import baker
from users.forms import UserForm, ProfileForm, ProfilePictureForm


class PersonDetailUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = baker.make(CustomUser)
        self.client.force_login(self.user)
        self.url = reverse("profile")

    def test_person_detail_update_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")
        self.assertIsInstance(response.context["user_form"], UserForm)
        self.assertIsInstance(response.context["profile_form"], ProfileForm)
        self.assertIsInstance(response.context["picture_form"], ProfilePictureForm)
