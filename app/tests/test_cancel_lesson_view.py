from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.messages import get_messages
from tutors.models import Lesson
from users.models import CustomUser
from app.views import CancelLessonView
from django.utils import timezone
import datetime
from model_bakery import baker
from datetime import time, date
from unittest.mock import patch

GGC_HANGOUTLINK = "https://calendar.google.com/"


class CancelLessonViewTest(TestCase):
    def setUp(self):
        self.mock_create_calendar_event = patch(
            "tutors.models.create_calendar_event",
            return_value=dict(hangoutLink=GGC_HANGOUTLINK),
        )
        self.mock_create_calendar_event.start()
        self.student = baker.make(CustomUser, is_tutor=False)
        self.tutor = baker.make(CustomUser, is_tutor=True)
        self.factory = RequestFactory()
        self.lesson = baker.make(
            Lesson,
            student=self.student,
            tutor=self.tutor,
            date=date.today(),
            start_time=time(10, 0),
            duration=60,
        )

    def tearDown(self):
        self.mock_create_calendar_event.stop()

    def test_tutor_can_cancel_lesson_before_start(self):
        # Set lesson date to future
        self.lesson.date = timezone.localdate() + datetime.timedelta(days=1)
        self.lesson.start_time = timezone.localtime().time()
        self.lesson.save()

        self.client.force_login(self.tutor)
        response = self.client.post(
            reverse("cancel_lesson", kwargs={'lesson_id': self.lesson.id}))

        self.lesson.refresh_from_db()

        self.assertEqual(self.lesson.status, Lesson.STATUS_CHOICES.CANCELLED)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lesson-list'))

    def test_tutor_cant_cancel_lesson_after_start(self):
        # Set lesson date to past
        self.lesson.date = timezone.localdate() - datetime.timedelta(days=1)
        self.lesson.start_time = timezone.localtime().time()
        self.lesson.save()

        self.client.force_login(self.tutor)
        response = self.client.post(
            reverse("cancel_lesson", kwargs={'lesson_id': self.lesson.id}))
        self.assertNotEqual(self.lesson.status, Lesson.STATUS_CHOICES.CANCELLED)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lesson-list'))
