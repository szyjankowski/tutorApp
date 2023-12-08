from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from datetime import datetime
from tutors.models import Lesson
from django.core.serializers import serialize
from django.views.generic.list import ListView


def index(request):
    if request.user.is_authenticated:
        return redirect("profile")
    return render(request, "app/index.html")


class LessonListView(ListView):  # show cancelled lessons and or completed
    model = Lesson
    template_name = "app/lesson-list.html"
    context_object_name = "lessons"

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
