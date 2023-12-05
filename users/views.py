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
from users.forms import UserForm, ProfileForm, ProfilePictureForm
from django.contrib.auth import get_user_model

# imports for mail
from users.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage


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

        if "profile_picture" in request.FILES and picture_form.is_valid():
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
            user.is_active = False
            user.save()
            activateEmail(request, user, user_form.cleaned_data.get("email"))
            return redirect("login")

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
            user.is_active = False
            user.save()
            activateEmail(request, user, user_form.cleaned_data.get("email"))
            return redirect("login")
    else:
        user_form = CustomUserCreationForm()
    return render(
        request,
        "users/student_signup.html",
        {"user_form": user_form},
    )


def activate(request, uidb64, token):
    user_model = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user_model.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):  # srapwdzic
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "You've activated your account, log in now.")
        return redirect("login")
    else:
        messages.error(request, "Link is invalid!")

    return redirect("landing-page")


def activateEmail(request, user, to_email):
    mail_subject = "Activate link - tutorApp"
    message = render_to_string(
        "users/email.html",
        {
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        },
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(
            request, f"Activate your account at {to_email} please check spam folder"
        )
    else:
        messages.error(
            request,
            "Something went wrong... check if you have entered correct email",
        )
