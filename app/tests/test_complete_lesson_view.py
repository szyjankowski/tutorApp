# from django.test import TestCase, Client
# from django.urls import reverse
# from django.contrib.messages import get_messages
# from wallet.models import Wallet, Transaction
# from tutors.models import Lesson
# from django.contrib.auth import get_user_model
# from unittest.mock import patch
# from unittest.mock import PropertyMock
# from model_bakery import baker
#
#
# class CompleteLessonViewTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user1 = get_user_model().objects.create_user(
#             email="student@user.com", password="foo", is_tutor=False
#         )
#         self.user2 = get_user_model().objects.create_user(
#             email="tutor@user.com", password="foo", is_tutor=True
#         )
#         self.lesson = baker.make('tutors.Lesson',
#                                  student=self.user1,
#                                  tutor=self.user2,
#                                  status=1)
#         self.wallet1 = Wallet.objects.create(user=self.user1, balance=100)
#         self.wallet2 = Wallet.objects.create(user=self.user2, balance=0)
#         self.url = reverse("complete-lesson", kwargs={"lesson_id": self.lesson.id})
#
#     def test_complete_lesson_success(self):
#         with patch('tutors.models.Lesson.cost', new_callable=PropertyMock) as mock_cost:
#             mock_cost.return_value = 50
#         response = self.client.post(self.url)
#         self.lesson.refresh_from_db()
#         self.wallet1.refresh_from_db()
#         self.wallet2.refresh_from_db()
#         self.assertEqual(self.lesson.status, Lesson.STATUS_CHOICES.COMPLETED)
#         self.assertEqual(self.wallet1.balance, 50)
#         self.assertEqual(self.wallet2.balance, 50)
#         self.assertEqual(Transaction.objects.count(), 1)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, reverse("lesson-list"))
#
#     def test_complete_lesson_insufficient_funds(self):
#         self.wallet1.balance = 40
#         self.wallet1.save()
#         response = self.client.post(self.url)
#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(
#             str(messages[0]),
#             "Student does not have funds on their wallet. Please contact them.",
#         )
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, reverse("lesson-list"))
#
#     def test_complete_lesson_not_found(self):
#         url = reverse("complete-lesson", kwargs={"lesson_id": 999})
#         response = self.client.post(url)
#         self.assertEqual(response.status_code, 404)
