from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views import generic
from users.forms import CustomUserCreationForm, CustomAuthenticationForm


# Create your views here.


class HomePage(TemplateView):
    template_name = "users/home.html"


class UserRegisterView(generic.CreateView):
    form_class = CustomAuthenticationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")


class UserLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")


class UserLogoutView(LogoutView):
    template_name = "users/logout.html"
    next_page = reverse_lazy("home")
