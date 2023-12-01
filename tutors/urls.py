from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from tutors.views import FindTutorView, LessonCreateView, LessonUpdateView

urlpatterns = [
    path("student/tutor-search/", FindTutorView.as_view(), name="tutor-search"),
    path(
        "tutor/lesson/create/<int:pk>", LessonCreateView.as_view(), name="create-lesson"
    ),
    path(
        "tutor/lesson/update/<int:pk>", LessonUpdateView.as_view(), name="update-lesson"
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
