# import pytest
# from django.http import Http404
# from django.urls import reverse_lazy
# from django.test import RequestFactory
# from django.contrib.auth import get_user_model
# from tutors.views import LessonUpdateView
# from tutors.models import Lesson
# from tutors.forms import CreateLessonForm
# from users.models import CustomUser
# from model_bakery import baker
# from django.test import TestCase, Client
# from django.shortcuts import reverse
# from unittest.mock import patch
#
#
# class LessonUpdateViewTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         # Ensure CustomUser has necessary attributes for the test
#         self.tutor = baker.make(CustomUser, is_tutor=True,
#                                 google_credentials={'refresh_token': 'mock_token'})
#         self.lesson = baker.make(Lesson, tutor=self.tutor)
#         self.client.force_login(self.tutor)
#         self.url = reverse("update-lesson", kwargs={"pk": self.lesson.pk})
#
#         # Patch the create_calendar_event function in the correct location
#         self.mock_calendar_event = patch('tutors.models.create_calendar_event').start()
#         self.mock_calendar_event.return_value = {"hangoutLink": "mock_link"}
#
#     def tearDown(self):
#         # Stop the patcher to clean up
#         patch.stopall()
#
#     def test_lesson_update_view_get(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "tutors/update-lesson.html")
#
#     @patch('tutors.models.create_calendar_event')
#     def test_lesson_create_view_post(self, mock_create_calendar_event):
#         mock_create_calendar_event.return_value = {"hangoutLink": "test_link"}
#
#         response = self.client.post(
#             self.url,
#             {
#                 "title": "Test Lesson",
#                 "description": "This is a test lesson",
#                 "date": "2022-12-31",
#                 "time": "12:00",
#                 "duration": 1,
#                 "price": 100,
#             },
#         )
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse("profile"))
#         self.assertEqual(Lesson.objects.count(), 1)
