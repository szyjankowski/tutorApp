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


class LessonListView(ListView):
    model = Lesson
    template_name = "app/lesson-list.html"
    context_object_name = "lessons"


class CalendarView(TemplateView):
    template_name = "app/calendar.html"

    def get_context_data(self, **kwargs):
        context = super(CalendarView, self).get_context_data(**kwargs)

        current_month = datetime.now().month
        current_year = datetime.now().year
        lessons = Lesson.objects.filter(
            date__year=current_year, date__month=current_month
        )
        lessons_json = serialize("json", lessons)

        context["date"] = datetime.now().strftime("%B %Y")
        context["lessons_json"] = lessons_json

        return context
