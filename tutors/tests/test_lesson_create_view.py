import pytest
from unittest.mock import patch
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from tutors.views import LessonCreateView
from tutors.models import CustomUser, Lesson
from tutors.forms import CreateLessonForm
from model_bakery import baker

GGC_HANGOUTLINK = "https://calendar.google.com/"


# nie dzialal nie wiem czemu
@pytest.fixture
def user(db):
    return get_user_model().objects.create_user(email="test@user.com", password="foo")


@pytest.fixture
def student(db):
    return baker.make(CustomUser)


@pytest.fixture
def form(user, student, mocker, db):
    cleaned_data = dict(tutor=user, student=student)

    return mocker.patch(
        "tutors.forms.CreateLessonForm", cleaned_data=cleaned_data, is_valid=True
    )


@pytest.mark.django_db
@patch(
    "tutors.models.create_calendar_event",
    return_value=dict(hangoutLink=GGC_HANGOUTLINK),
)
def test_lesson_create_view(mock_create_calendar_event, user, student, form):
    view = LessonCreateView()
    view.request = RequestFactory().get("/")
    view.request.user = user
    view.kwargs = {"pk": student.pk}

    view.form_valid(form)

    assert form.instance.tutor == user
    assert form.instance.student == student
