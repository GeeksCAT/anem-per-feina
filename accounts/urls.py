from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import LoginView, LogoutView, RegisterEmployerView

app_name = "accounts"

urlpatterns = [
    path("employer/register", RegisterEmployerView.as_view(), name="employer-register"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("login", LoginView.as_view(), name="login"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
