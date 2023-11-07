from django.urls import path
from tutors.views import FindTutorView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("tutor-search/", FindTutorView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
