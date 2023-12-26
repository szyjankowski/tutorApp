from django.shortcuts import render, get_object_or_404, redirect
from tutors.models import Lesson
from django.views.generic.list import ListView
from django.views import View
from django.db import transaction
from wallet.models import Wallet, Transaction, TRANSACTION_TYPES
from django.utils import timezone
from datetime import datetime
from django.contrib import messages


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
        queryset = super().get_queryset()
        if self.request.user.is_tutor:
            return queryset.filter(tutor=self.request.user.id).order_by(
                "date", "start_time"
            )
        else:
            return queryset.filter(student=self.request.user.id).order_by(
                "date", "start_time"
            )


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


class CancelLessonView(View):
    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        now = timezone.now()
        start_datetime = datetime.combine(lesson.date, lesson.start_time)

        if now < start_datetime:
            lesson.status = Lesson.STATUS_CHOICES.CANCELLED
            lesson.save()
            # Redirect to a cancelled confirmation page
            return redirect("cancelled_lesson_view")

        # Redirect to an error page if cancellation is not allowed
        return redirect("error_view")
