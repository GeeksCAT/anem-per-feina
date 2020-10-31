from django.urls import include, path

from .views.employer import DashboardView, JobCreateView, JobDeleteView, filled
from .views.home import ContactView, HomeView, JobDetailsView, JobListView, SearchView

app_name = "jobs"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("search", SearchView.as_view(), name="searh"),
    path(
        "employer/dashboard/",
        include(
            [
                path("", DashboardView.as_view(), name="employer-dashboard"),
                path("mark-filled/<int:job_id>", filled, name="job-mark-filled"),
                path(
                    "delete/<int:pk>",
                    JobDeleteView.as_view(),
                    name="employer-dashboard-delete-offer",
                ),
            ]
        ),
    ),
    path("jobs", JobListView.as_view(), name="jobs"),
    path("jobs/<int:id>", JobDetailsView.as_view(), name="jobs-detail"),
    path("contact-us", ContactView.as_view(), name="contact-us"),
    path("employer/jobs/create", JobCreateView.as_view(), name="employer-jobs-create"),
]
