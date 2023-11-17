from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from tutors.models import TutorProfile
from tutors.models import PriceList
from django.contrib.auth.decorators import login_required


@login_required
def tutor_profile_view(request):
    profile = get_object_or_404(TutorProfile, user=request.user)
    return render(request, "tutors/tutor_profile.html", {"tutor_profile": profile})


@login_required
class FindTutorView(ListView):
    model = TutorProfile
    template_name = "tutors/tutor-search.html"
    context_object_name = "tutors"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subject_choices"] = PriceList.SUBJECTS
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filter_queryset(queryset)
        return queryset

    def filter_queryset(self, queryset):
        subject_ids = self.request.GET.getlist("subject")
        if subject_ids:
            queryset = queryset.filter(
                pricelist_set__subject__in=subject_ids
            ).distinct()
        return queryset


@login_required
def tutor_profile(request, tutor_id):
    tutor = get_object_or_404(TutorProfile, pk=tutor_id)
    pricelists = tutor.pricelists
    return render(
        request, "tutors/tutor-profile.html", {"tutor": tutor, "pricelists": pricelists}
    )
