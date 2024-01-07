from celery import shared_task
from django.utils import timezone
from tutors.models import Lesson
from datetime import timedelta


@shared_task
def delete_cancelled_lessons():
    three_days_ago = timezone.now() - timedelta(days=3)
    Lesson.objects.filter(
        status=Lesson.STATUS_CHOICES.CANCELLED, cancelled_at__lte=three_days_ago
    ).delete()
