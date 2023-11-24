from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from users.models import CustomUser
from django import forms
from tutors.models import Profile
from django.forms import ModelForm

User = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"autofocus": True})
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        return username.lower()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


# class StudentProfileForm(ModelForm):
#     class Meta:
#         model = StudentProfile
#         fields = ["description_student"]


class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name"]
