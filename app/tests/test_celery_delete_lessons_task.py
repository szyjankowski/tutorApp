from django.test import TestCase
from tutors.models import Lesson
from app.tasks import delete_cancelled_lessons
from model_bakery import baker
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch

GGC_HANGOUTLINK = "https://calendar.google.com/"


class CeleryDeleteCancelledLessonsTest(TestCase):
    def setUp(self):
        self.mock_create_calendar_event = patch(
            "tutors.models.create_calendar_event",
            return_value=dict(hangoutLink=GGC_HANGOUTLINK),
        )
        self.mock_create_calendar_event.start()

        # swtich to comments
        lesson_to_delete = baker.make(
            Lesson,
            status=Lesson.STATUS_CHOICES.CANCELLED,
            cancelled_at=timezone.now() - timedelta(10),
        )

        lesson_to_delete2 = baker.make(
            Lesson,
            status=Lesson.STATUS_CHOICES.CANCELLED,
            cancelled_at=timezone.now() - timedelta(15),
        )

        lesson_to_stay = baker.make(
            Lesson,
            status=Lesson.STATUS_CHOICES.CANCELLED,
            cancelled_at=timezone.now() - timedelta(1),
        )

    def tearDown(self):
        self.mock_create_calendar_event.stop()
        super().tearDown()

    def test_delete_cancelled_lessons(self):
        # Number of lessons before running the task
        lessons_before = Lesson.objects.count()

        delete_cancelled_lessons()

        # Number of lessons after running the task
        lessons_after = Lesson.objects.count()

        # Check if the number of lessons is as expected
        self.assertNotEqual(lessons_before, lessons_after)
        self.assertEqual(lessons_after, 1)
