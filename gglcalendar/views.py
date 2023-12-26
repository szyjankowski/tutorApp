from django.shortcuts import redirect
from django.views.generic import TemplateView
from datetime import datetime
from tutors.models import Lesson
from django.core.serializers import serialize
import os
from django.http import HttpResponseBadRequest
from django.db.models import Q

# imports for google api
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow


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
    logged_user = request.user

    # user.google_credentials = {
    #     "token": credentials.token,
    #     "refresh_token": credentials.refresh_token,
    #     "token_uri": credentials.token_uri,
    #     "client_id": credentials.client_id,
    #     "client_secret": credentials.client_secret,
    #     "scopes": credentials.scopes,
    # }

    logged_user.google_credentials = {"refresh_token": credentials.refresh_token}

    request.session["google_credentials_temp"] = {
        "token": credentials.token,
    }
    logged_user.save()

    return redirect("calendar")


class CalendarView(TemplateView):
    template_name = "gglcalendar/calendar.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_tutor:
            return queryset.filter(tutor=self.request.user.id)
        else:
            return queryset.filter(student=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(CalendarView, self).get_context_data(**kwargs)

        current_month = datetime.now().month
        current_year = datetime.now().year

        lessons = Lesson.objects.filter(
            Q(tutor=self.request.user.id) | Q(student=self.request.user.id),
            date__year=current_year,
            date__month=current_month,
        )

        lessons_json = serialize("json", lessons)

        context["date"] = datetime.now().strftime("%B %Y")
        context["lessons_json"] = lessons_json

        return context
