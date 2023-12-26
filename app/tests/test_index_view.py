import django.test.client
from django.test import TestCase
from users.models import CustomUser
from model_bakery import baker
from django.urls import reverse


class IndexViewTest(TestCase):
    def setUp(self):
        self.user = baker.make(CustomUser)

    def test_index_view_with_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("home"))
        self.assertRedirects(response, reverse("profile"))

    def test_index_view_with_unauthenticated_user(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/index.html")
