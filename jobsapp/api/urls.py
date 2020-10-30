from django.urls import path, re_path

from .views.jobs import JobsViewDetails, JobsViewList
from .views.users import UsersViewDetails, UsersViewsList

urlpatterns = [
    re_path("jobs/?$", JobsViewList.as_view(), name="jobs-list"),
    path("jobs/<int:pk>", JobsViewDetails.as_view(), name="job-detail"),
    re_path("users/?$", UsersViewsList.as_view(), name="users-list"),
    path("users/<int:pk>", UsersViewDetails.as_view(), name="user-detail"),
]
