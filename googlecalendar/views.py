from django.shortcuts import render
from django.views.generic import TemplateView
from datetime import datetime
from tutors.models import Lesson
from django.core.serializers import serialize
from django.views.generic.list import ListView


# Create your views here.

from google_auth_oauthlib.flow import Flow
from django.shortcuts import redirect


def start_auth(request):
    # Create the flow using the client secrets file from the Google API Console.
    flow = Flow.from_client_secrets_file(
        "client_secrets.json",
        scopes=["https://www.googleapis.com/auth/calendar"],
        redirect_uri="http://localhost:8000/callback",
    )

    # Generate URL for request to Google's OAuth 2.0 server.
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type="offline",
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes="true",
    )

    # Store the state so the callback can verify the auth server response.
    request.session["state"] = state

    return redirect(authorization_url)


def callback(request):
    state = request.session["state"]

    flow = Flow.from_client_secrets_file(
        "client_secrets.json",
        scopes=["https://www.googleapis.com/auth/calendar"],
        state=state,
        redirect_uri="http://localhost:8000/callback",
    )

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    request.session["credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }

    return redirect("create_event")


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
