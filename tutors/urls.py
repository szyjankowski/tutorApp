from django.urls import path
from tutors.views import tutor_profile_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [path("tutor/profile/", tutor_profile_view, name="tutor-profile")]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
