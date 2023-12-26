# Create your tests here.
# FILEPATH: /c:/python/tutorAppFiles/tutorApp/gglcalendar/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from model_bakery import baker  # Import bakery
from datetime import datetime
from tutors.models import Lesson
from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware


class TestCalendarView(TestCase):
    def setUp(self):
        self.client = Client()
        # Use bakery to create a user instance
        self.user = baker.make(get_user_model(), email="test@user.com")

    def test_calendar_view(self):  # More descriptive name for the test
        self.client.force_login(self.user)  # Using force_login for simplicity
        response = self.client.get(reverse("calendar"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "gglcalendar/calendar.html")


class TestGoogleAuthFunctions(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = baker.make(get_user_model(), email="test@user.com")
        self.client.force_login(self.user)

    @patch("gglcalendar.views.Flow")
    def test_start_auth(self, MockFlow):
        mock_flow = MagicMock()
        MockFlow.from_client_secrets_file.return_value = mock_flow
        mock_flow.authorization_url.return_value = ("http://auth-url", "state")

        response = self.client.get(reverse("start-auth"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "http://auth-url")
        self.assertEqual(self.client.session["state"], "state")
