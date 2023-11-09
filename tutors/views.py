from django.shortcuts import render
from django.views.generic.list import ListView
from tutors.models import TutorProfile


# Create your views here.


class FindTutorView(ListView):
    model = TutorProfile
    template_name = "tutors/tutor-search.html"
    context_object_name = "tutors"

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = self.filter_queryset(queryset)
    #     return queryset
    #
    # def filter_queryset(self, queryset):
    #     if subject := (self.request.GET.getlist('subject')):
    #         queryset = queryset.filter()
