from django.urls import path, re_path

from .views.common import (
    AboutUs,
    ContactUs,
    JobsViewDetails,
    JobsViewList,
    JobViewSet,
    SearchApiView,
    UsersList,
)

urlpatterns = [
    re_path("jobs/?$", JobsViewList.as_view(), name="jobs-list"),
    path("jobs/<int:pk>", JobsViewDetails.as_view(), name="job-detail"),
    re_path("users/?$", UsersList.as_view(), name="users-list"),
    path("users/<int:pk>", UsersList.as_view(), name="user-detail"),
    path("search/", SearchApiView.as_view()),
    path("contact-us", ContactUs.as_view()),
    path("about-us", AboutUs.as_view(), name="about-us"),
]
