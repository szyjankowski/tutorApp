from django.urls import path
from app.views import index as index_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [path("", index_view, name="home")]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
