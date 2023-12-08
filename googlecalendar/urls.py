from django.urls import path
from app.views import index as index_view, LessonListView
from googlecalendar.views import CalendarView, start_auth, callback
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("calendar/", CalendarView.as_view(), name="calendar"),
    path("startauth/", start_auth, name="start-auth"),
    path("callback/", callback, name="callback"),
    # path("createevent/", create_event, name="create-event"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
