from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from users.models import CustomUser, Profile
from django import forms
from django.forms import ModelForm

User = get_user_model()


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_picture"]


class CombinedForm(forms.ModelForm):
    description = forms.CharField()  # Add other fields from Profile as needed

    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "description"]

    def save(self, commit=True):
        user = super().save(commit=False)
        profile_description = self.cleaned_data.pop("description", None)

        if commit:
            user.save()
            user.profile.description = profile_description
            user.profile.save()

        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["description"]


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
