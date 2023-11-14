from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from users.forms import CustomUserCreationForm, TutorProfileForm, StudentProfileForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import StudentProfile


# Create your views here.

@login_required
def student_profile_view(request):
    # Ensure that we have a studentprofile related to the current user
    student_profile = get_object_or_404(StudentProfile, user=request.user)

    # Render the student profile template with the student profile context
    return render(
        request, "users/student_profile.html", {"student_profile": student_profile}
    )


class UserLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")


class UserLogoutView(LogoutView):
    template_name = "users/logout.html"
    next_page = reverse_lazy("home")


def tutor_signup(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        profile_form = TutorProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            tutor_profile = profile_form.save(commit=False)
            tutor_profile.user = user
            tutor_profile.save()
            return redirect("tutor-profile", tutor_name=user.pk)
    else:
        user_form = CustomUserCreationForm()
        profile_form = TutorProfileForm()
    return render(
        request,
        "users/tutor_signup.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


def student_signup(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        profile_form = StudentProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            student_profile = profile_form.save(commit=False)
            student_profile.user = user
            student_profile.save()
            # Redirect to a success page.
            return redirect("student-profile", student_name=user.pk)
    else:
        user_form = CustomUserCreationForm()
        profile_form = StudentProfileForm()
    return render(
        request,
        "users/student_signup.html",
        {"user_form": user_form, "profile_form": profile_form},
    )
