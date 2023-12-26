from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomUser
from users.forms import UserForm, ProfileForm, ProfilePictureForm
from model_bakery import baker


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

    def test_person_detail_update_view_post(self):
        post_data = {
            "email": "email@test.com",
            "first_name": "New",
            "last_name": "Name",
        }

        response = self.client.post(self.url, post_data)

        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "email@test.com")
        self.assertEqual(self.user.first_name, "New")
        self.assertEqual(self.user.last_name, "Name")
