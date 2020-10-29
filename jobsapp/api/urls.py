from rest_framework.routers import DefaultRouter

from django.urls import path

from .views.common import ContactUs, JobViewSet, SearchApiView,  AboutUs,

router = DefaultRouter()
router.register("jobs", JobViewSet)

urlpatterns = [
    path("search/", SearchApiView.as_view()),
    path("contact-us", ContactUs.as_view()),
    path("about-us", AboutUs.as_view(), name="about-us"),
]

urlpatterns += router.urls
