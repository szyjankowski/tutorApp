from django.urls import path
from app.views import index as index_view, LessonListView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", index_view, name="home"),
    path("lessons/", LessonListView.as_view(), name="lesson-list"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
