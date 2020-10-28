from rest_framework.routers import DefaultRouter

from django.urls import path

from .views.common import JobViewSet, SearchApiView, about_us, contact_us

router = DefaultRouter()
router.register("jobs", JobViewSet)

urlpatterns = [
    path("search/", SearchApiView.as_view()),
    path("about-us", about_us),
    path("contact-us", contact_us),
]

urlpatterns += router.urls
