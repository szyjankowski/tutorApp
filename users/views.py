from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from users.forms import CustomUserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from users.models import StudentProfile, CustomUser
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/profile.html"
    context_object_name = "user"
    login_url = reverse_lazy('login')

    # redirect_field_name = reverse_lazy('login')

    def get_object(self, queryset=None):
        return self.request.user


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
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_tutor = True
            user.save()
            return redirect("tutor-profile", tutor_name=user.pk)
    else:
        user_form = CustomUserCreationForm()
    return render(
        request,
        "users/tutor_signup.html",
        {"user_form": user_form},
    )


def student_signup(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_tutor = False
            user.save()
            # Redirect to a success page.
            return redirect("login")
    else:
        user_form = CustomUserCreationForm()
    return render(
        request,
        "users/student_signup.html",
        {"user_form": user_form},
    )
