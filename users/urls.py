from django.urls import path
from users.views import (
    UserLoginView,
    UserLogoutView,
    student_signup,
    tutor_signup,
    student_profile_view,
)
from django.conf import settings
from django.conf.urls.static import static
from tutors.views import FindTutorView

urlpatterns = [
    path("student/tutor-search/", FindTutorView.as_view(), name="tutor-search"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("signup/tutor/", tutor_signup, name="tutor-signup"),
    path("signup/student/", student_signup, name="student-signup"),
    path("student/profile", student_profile_view, name="student-profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
