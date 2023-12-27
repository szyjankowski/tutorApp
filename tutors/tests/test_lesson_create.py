from django.urls import reverse
from django.test import TestCase, RequestFactory, Client
from tutors.models import Lesson
from users.models import CustomUser
from model_bakery import baker
from unittest.mock import patch

GGC_HANGOUTLINK = "https://calendar.google.com/"


class LessonCreateViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.tutor = baker.make(CustomUser, is_tutor=True)
        self.student = baker.make(CustomUser, is_tutor=False)
        self.mock_create_calendar_event = patch(
            "tutors.models.create_calendar_event",
            return_value=dict(hangoutLink=GGC_HANGOUTLINK),
        )
        self.mock_create_calendar_event.start()

    def tearDown(self):
        self.mock_create_calendar_event.stop()

    def test_tutor_can_create_lesson(self):
        self.client.force_login(self.tutor)
        response = self.client.post(
            reverse("create-lesson", kwargs={"pk": self.student.id}),
            {
                "title": "Test Lesson",
                "description": "This is a test lesson",
                "duration": 10,
                "date": "2022-12-31",
                "start_time": "10:00",
                "tutor": self.tutor,
                "student": self.student,
                "subject": 1,
                "status": 1,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertRedirects(response, reverse("profile"))
