from django import forms
from django.contrib.auth import get_user_model
from tutors.models import Lesson

User = get_user_model()


class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "description", "duration", "date", "start_time", "subject"]
        # calendar link will be generated
