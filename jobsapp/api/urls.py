from django.urls import path, re_path

from .views.common import (
    AboutUs,
    ContactUs,
    JobsViewDetails,
    JobsViewList,
    JobViewSet,
    SearchApiView,
)

urlpatterns = [
    re_path("jobs/?$", JobsViewList.as_view(), name="jobs-list"),
    path("jobs/<int:pk>", JobsViewDetails.as_view(), name="jobs-detail"),
    path("search/", SearchApiView.as_view()),
    path("contact-us", ContactUs.as_view()),
    path("about-us", AboutUs.as_view(), name="about-us"),
]
