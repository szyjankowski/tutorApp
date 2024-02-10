from django.views.generic.list import ListView
from users.models import Profile
from tutors.models import PriceList, Lesson
from django.views.generic.edit import CreateView
from tutors.forms import CreateLessonForm, CreatePriceListForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from app.mixins import IsStudentMixin, IsTutorMixin
from django.shortcuts import get_object_or_404
from users.models import CustomUser
from django.views.generic.edit import UpdateView
from django.http import Http404


class FindTutorView(IsStudentMixin, LoginRequiredMixin, ListView):
    """View for students to look for tutors, only available for students."""

    model = Profile
    template_name = "tutors/tutor-search.html"
    context_object_name = "tutors"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subject_choices"] = PriceList.SUBJECTS
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = self.filter_queryset_only_tutors(queryset)
        return queryset

    def filter_queryset(self, queryset):
        subject_ids = self.request.GET.getlist("subject")
        if subject_ids:
            queryset = queryset.filter(
                pricelist_set__subject__in=subject_ids
            ).distinct()
        return queryset

    @staticmethod
    def filter_queryset_only_tutors(queryset):
        queryset = queryset.filter(user__is_tutor=True)
        return queryset


class LessonCreateView(IsTutorMixin, LoginRequiredMixin, CreateView):
    model = Lesson
    template_name = "tutors/create-lesson.html"
    form_class = CreateLessonForm
    success_url = reverse_lazy("profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student_user"] = get_object_or_404(
            CustomUser, pk=self.kwargs.get("pk")
        )
        return context

    def form_valid(self, form):
        form.instance.tutor = self.request.user
        form.instance.student = get_object_or_404(CustomUser, pk=self.kwargs.get("pk"))
        form.instance.calendar_meet_link = "TODO"
        form.instance.status = 1

        return super().form_valid(form)


class LessonUpdateView(UpdateView):
    model = Lesson
    template_name = "tutors/update-lesson.html"
    form_class = CreateLessonForm
    success_url = reverse_lazy("profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()
        context["lesson"] = lesson
        context["student_user"] = lesson.student
        return context

    def dispatch(self, request, *args, **kwargs):
        lesson = self.get_object()
        if lesson.tutor != request.user:
            raise Http404("You do not have permission to edit this lesson.")
        return super().dispatch(request, *args, **kwargs)


class CreatePriceListView(IsTutorMixin, CreateView):
    model = PriceList
    template_name = "tutors/create-pricelist.html"
    form_class = CreatePriceListForm
    success_url = reverse_lazy("profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subjects = PriceList.SUBJECTS
        context["subjects"] = subjects
        return context

    def form_valid(self, form):
        user = self.request.user
        form.instance.tutor = user.profile
        return super().form_valid(form)
