from django.shortcuts import render
from django.views.generic.list import ListView
from tutors.models import TutorProfile


# Create your views here.


class FindTutorView(ListView):
    model = TutorProfile
    template_name = "tutors/tutor-search.html"
