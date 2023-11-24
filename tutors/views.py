from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from tutors.models import Profile
from tutors.models import PriceList
from django.contrib.auth.decorators import login_required


@login_required
def tutor_profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, "tutors/tutor_profile.html", {"tutor_profile": profile})


class FindTutorView(ListView):
    model = Profile
    template_name = "app/tutor-search.html"
    context_object_name = "tutors"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subject_choices"] = PriceList.SUBJECTS
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = self.only_tutors_filter_queryset(queryset)
        return queryset

    def filter_queryset(self, queryset):
        subject_ids = self.request.GET.getlist("subject")
        if subject_ids:
            queryset = queryset.filter(
                pricelist_set__subject__in=subject_ids
            ).distinct()
        return queryset

    def only_tutors_filter_queryset(self, queryset):
        queryset = super().get_queryset()
        queryset = queryset.filter(user__is_tutor=True)
        return queryset


@login_required
def tutor_profile(request, tutor_id):
    tutor = get_object_or_404(Profile, pk=tutor_id)
    pricelists = tutor.pricelists
    return render(
        request, "tutors/tutor-profile.html", {"tutor": tutor, "pricelists": pricelists}
    )
