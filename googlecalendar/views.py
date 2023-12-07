from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from datetime import datetime
from tutors.models import Lesson
from django.core.serializers import serialize
from django.views.generic.list import ListView
import os
from django.contrib import messages

# imports for google api
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2 import id_token


def create_calendar_event(lesson):
    # Load the tutor's credentials from the user model
    credentials = Credentials.from_authorized_user_info(lesson.tutor.google_credentials)

    # Build the service object
    service = build("calendar", "v3", credentials=credentials)

    # Convert the lesson start and end times to RFC3339 format
    start_time = datetime.combine(lesson.date, lesson.start_time).isoformat()
    end_time = datetime.combine(lesson.date, lesson.end_time).isoformat()

    # Create the event object
    event = {
        "summary": lesson.title,
        "description": lesson.description,
        "start": {
            "dateTime": start_time,
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "UTC",
        },
    }

    # Call the Calendar API to create the event
    event = service.events().insert(calendarId="primary", body=event).execute()

    # Save the Google Meet link in the lesson
    lesson.calendar_meet_link = event["hangoutLink"]
    lesson.save()


def start_auth(request):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    flow = Flow.from_client_secrets_file(
        "client_secrets.json",
        scopes=["https://www.googleapis.com/auth/calendar"],
        redirect_uri="http://localhost:8000/callback",
    )

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
    )

    request.session["state"] = state

    return redirect(authorization_url)


def callback(request):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    if "state" not in request.session:
        return redirect("start-auth")

    state = request.session["state"]

    if request.GET.get("state") != state:
        return HttpResponseBadRequest("State mismatch")

    flow = Flow.from_client_secrets_file(
        "client_secrets.json",
        scopes=["https://www.googleapis.com/auth/calendar"],
        state=state,
        redirect_uri="http://localhost:8000/callback",
    )

    # authorization server to fetch tokens(credentials)
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    user = request.user

    user.google_credentials = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }

    user.save()

    return redirect("create-event")


def create_event(request):
    # Load the user's credentials from the session
    credentials = Credentials.from_authorized_user_info(request.user.google_credentials)

    # Build the calendar service
    service = build("calendar", "v3", credentials=credentials)

    # Define the event
    event = {
        "summary": "Meeting with tutor",
        "start": {
            "dateTime": "2022-01-01T10:00:00",
            "timeZone": "America/Los_Angeles",
        },
        "end": {
            "dateTime": "2022-01-01T11:00:00",
            "timeZone": "America/Los_Angeles",
        },
    }

    # Create the event
    event = service.events().insert(calendarId="primary", body=event).execute()
    messages.success(request, "Event created successfully")

    return redirect("calendar")


class CalendarView(TemplateView):
    template_name = "googlecalendar/calendar.html"

    def get_queryset(self):
        if self.request.user.is_tutor:
            queryset = super().get_queryset()
            return queryset.filter(tutor=self.request.user.id)
        else:
            queryset = super().get_queryset()
            return queryset.filter(student=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(CalendarView, self).get_context_data(**kwargs)

        current_month = datetime.now().month
        current_year = datetime.now().year
        if self.request.user.is_tutor:
            lessons = Lesson.objects.filter(
                tutor=self.request.user.id,
                date__year=current_year,
                date__month=current_month,
            )

        else:
            lessons = Lesson.objects.filter(
                student=self.request.user.id,
                date__year=current_year,
                date__month=current_month,
            )

        lessons_json = serialize("json", lessons)

        context["date"] = datetime.now().strftime("%B %Y")
        context["lessons_json"] = lessons_json

        return context
