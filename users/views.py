from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from users.forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from users.models import CustomUser
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView
from users.forms import UserForm, ProfileForm, ProfilePictureForm


class PersonDetailUpdateView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"

    def get(self, request, *args, **kwargs):
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        picture_form = ProfilePictureForm(instance=request.user.profile)
        return self.render_to_response(
            {
                "user_form": user_form,
                "profile_form": profile_form,
                "picture_form": picture_form,
            }
        )

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        picture_form = ProfilePictureForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if "profile_picture" in request.FILES:
            if picture_form.is_valid():
                picture_form.save()

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

        return redirect("profile")  # Replace 'profile' with your success URL


class PublicProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/public-profile.html"
    context_object_name = "current_profile_user"
    login_url = reverse_lazy("login")

    def get_object(self, queryset=None):
        user = get_object_or_404(CustomUser, pk=self.kwargs.get("pk"))

        if user.is_tutor:
            return user
        else:
            raise Http404("User is not a tutor.")


class UserLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        messages.success(self.request, "You have successfully logged in.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Login failed. Please try again.", extra_tags="danger"
        )
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    template_name = "users/logout.html"
    next_page = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)


def tutor_signup(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_tutor = True
            user.save()

            return redirect("profile")
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
