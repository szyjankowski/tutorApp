from django.shortcuts import render, get_object_or_404, redirect
from tutors.models import Lesson
from django.views.generic.list import ListView
from django.views import View
from django.db import transaction
from wallet.models import Wallet, Transaction, TRANSACTION_TYPES
from datetime import datetime
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
import datetime


def index(request):
    if request.user.is_authenticated:
        return redirect("profile")
    return render(request, "app/index.html")


class LessonListView(ListView):  # show cancelled lessons and or completed
    model = Lesson
    template_name = "app/lesson-list.html"
    context_object_name = "lessons"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_time"] = timezone.now()
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        q = Q(tutor=user.id) if user.is_tutor else Q(student=user.id)
        return queryset.filter(q).order_by("date", "start_time")


class CompleteLessonView(View):
    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)

        with transaction.atomic():
            cost = lesson.cost
            student_wallet = Wallet.objects.get(user=lesson.student)
            tutor_wallet = Wallet.objects.get(user=lesson.tutor)

            # notifications ze nie masz hajsu

            if student_wallet.balance < cost:
                messages.error(
                    request,
                    "Student does not have funds on their wallet. Please contact them.",
                )
                return redirect("lesson-list")
            lesson.status = Lesson.STATUS_CHOICES.COMPLETED
            lesson.save()

            # Update wallets and create a transaction record
            student_wallet.balance -= cost
            student_wallet.save()
            tutor_wallet.balance += cost
            tutor_wallet.save()

            Transaction.objects.create(
                sender=lesson.student,
                receiver=lesson.tutor,
                transaction_type=TRANSACTION_TYPES.TRANSFER,
                amount=cost,
            )

        return redirect("lesson-list")


# the cancel button is not there when someone tries to cancel after the time.

class CancelLessonView(View):
    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        start_datetime = timezone.make_aware(
            datetime.datetime.combine(lesson.date, lesson.start_time),
            timezone.get_current_timezone()
        )

        # If current time is before the lesson start time, allow cancellation
        if timezone.now() < start_datetime:
            lesson.status = Lesson.STATUS_CHOICES.CANCELLED
            lesson.save()
            return redirect("lesson-list")

        # If current time is equal to or after start time, do not allow cancellation
        messages.error(self.request, "You can't cancel lesson after start")
        return redirect("lesson-list")
