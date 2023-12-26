from django.urls import path
from app.views import (
    index as index_view,
    LessonListView,
    CompleteLessonView,
    CancelLessonView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", index_view, name="home"),
    path("lessons/", LessonListView.as_view(), name="lesson-list"),
    path(
        "lesson/<int:lesson_id>/cancel/",
        CancelLessonView.as_view(),
        name="cancel_lesson",
    ),
    path(
        "lesson/<int:lesson_id>/complete/",
        CompleteLessonView.as_view(),
        name="complete_lesson",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
