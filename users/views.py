from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from users.forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from users.models import CustomUser
from tutors.models import Profile
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class PersonDetailUpdateView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"

    def post(self, request, *args, **kwargs):  # ugly way of handling this
        #  as using forms only caused problems
        # because of multiple models - customuser and given profile.
        user = self.request.user

        if description_data := request.POST.get("description"):
            user.profile.description = description_data
            user.profile.save()

        if email_data := request.POST.get("email"):
            user.email = email_data
            user.save()

        if first_name_data := request.POST.get("first_name"):
            user.first_name = first_name_data
            user.save()

        if last_name_data := request.POST.get("last_name"):
            user.last_name = last_name_data
            user.save()

        return redirect("profile")


# class ProfileView(LoginRequiredMixin, DetailView):
#     model = CustomUser
#     template_name = "users/profile.html"
#     context_object_name = "user"
#     login_url = reverse_lazy("login")
#
#     def get_object(self, queryset=None):
#         return self.request.user


class PublicProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/public-profile.html"
    context_object_name = "user"
    login_url = reverse_lazy("login")

    def get_object(self, queryset=None):
        return CustomUser.objects.get(id=self.kwargs.get("pk"))


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
