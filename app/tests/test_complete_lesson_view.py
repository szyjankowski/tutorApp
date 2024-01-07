from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.messages.storage.fallback import FallbackStorage
from django.db import transaction
from tutors.models import Lesson, CustomUser
from wallet.models import Wallet, Transaction
from app.views import CompleteLessonView
from model_bakery import baker
from unittest.mock import patch
from unittest import mock
from datetime import time, date

GGC_HANGOUTLINK = "https://calendar.google.com/"
GOOGLE_CREDENTIALS = {
    "refresh_token": "some_refresh_token",
}


class CompleteLessonViewTest(TestCase):
    def setUp(self):
        self.mock_create_calendar_event = patch(
            "tutors.models.create_calendar_event",
            return_value=dict(hangoutLink=GGC_HANGOUTLINK),
        )
        self.mock_create_calendar_event.start()

        self.patcher = mock.patch(
            "tutors.models.Lesson.cost", new_callable=mock.PropertyMock
        )
        self.mock_my_property = self.patcher.start()
        self.mock_my_property.return_value = 100

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
        self.patcher.stop()
        self.mock_create_calendar_event.stop()
        super().tearDown()

    def test_complete_lesson_insufficient_funds(self):
        self.client.force_login(self.tutor)
        response = self.client.post(
            reverse("complete_lesson", kwargs={"lesson_id": self.lesson.id})
        )
        self.lesson.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("lesson-list"))

    def test_complete_lesson_success(self):
        self.student.wallet.balance = 200
        self.student.wallet.save()

        self.client.force_login(self.tutor)
        response = self.client.post(
            reverse("complete_lesson", kwargs={"lesson_id": self.lesson.id})
        )

        with transaction.atomic():
            self.lesson.refresh_from_db()
            self.student.wallet.refresh_from_db()
            self.tutor.wallet.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("lesson-list"))
        self.assertEqual(self.lesson.status, Lesson.STATUS_CHOICES.COMPLETED)
        self.assertTrue(self.student.wallet.balance < 200)
        self.assertTrue(self.tutor.wallet.balance > 50)
        self.assertTrue(
            Transaction.objects.filter(
                sender=self.student, receiver=self.tutor
            ).exists()
        )
