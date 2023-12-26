from django.urls import reverse
from django.test import TestCase, Client
from tutors.models import Lesson
from users.models import CustomUser
from model_bakery import baker


class LessonCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.tutor = baker.make(CustomUser, is_tutor=True)
        self.student = baker.make(CustomUser, is_tutor=False)
        self.client.force_login(self.tutor)
        self.url = reverse("create-lesson", kwargs={"pk": self.student.pk})

    def test_have_access_to_lesson_create_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tutors/create-lesson.html")

    def test_can_create_lesson_object(self):
        response = self.client.post(
            self.url,
            {
                "title": "Test Lesson",
                "description": "This is a test lesson",
                "date": "2022-12-31",
                "time": "12:00",
                "duration": 1,
                "price": 100,
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertRedirects(response, reverse("profile"))
        self.assertEqual(Lesson.objects.count(), 1)
