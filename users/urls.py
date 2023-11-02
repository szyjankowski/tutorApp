from django.urls import path
from users.views import UserLoginView, UserLogoutView, HomePage, UserRegisterView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
