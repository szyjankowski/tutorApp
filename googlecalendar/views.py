from django.shortcuts import render
from django.views.generic import TemplateView
from datetime import datetime
from tutors.models import Lesson
from django.core.serializers import serialize
from django.views.generic.list import ListView


# Create your views here.


class CalendarView(TemplateView):
    template_name = "googlecalendar/calendar.html"

    def get_queryset(self):
        if self.request.user.is_tutor:
            queryset = super().get_queryset()
            return queryset.filter(tutor=self.request.user.id)
        else:
            queryset = super().get_queryset()
            return queryset.filter(student=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(CalendarView, self).get_context_data(**kwargs)

        current_month = datetime.now().month
        current_year = datetime.now().year
        if self.request.user.is_tutor:
            lessons = Lesson.objects.filter(
                tutor=self.request.user.id,
                date__year=current_year,
                date__month=current_month,
            )

        else:
            lessons = Lesson.objects.filter(
                student=self.request.user.id,
                date__year=current_year,
                date__month=current_month,
            )

        lessons_json = serialize("json", lessons)

        context["date"] = datetime.now().strftime("%B %Y")
        context["lessons_json"] = lessons_json

        return context
