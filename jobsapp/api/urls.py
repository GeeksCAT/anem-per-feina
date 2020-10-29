from rest_framework.routers import DefaultRouter

from django.urls import path

from .views.common import AboutUs, ContactUs, JobViewSet, SearchApiView

router = DefaultRouter()
router.register("jobs", JobViewSet)

urlpatterns = [
    path("search/", SearchApiView.as_view()),
    path("about-us", AboutUs.as_view()),
    path("contact-us", ContactUs.as_view()),
]

urlpatterns += router.urls
