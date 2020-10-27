from rest_framework.routers import DefaultRouter

from django.urls import path

from .views.common import JobViewSet, SearchApiView, about_us, contact_us
from .views.employee import AppliedJobsAPIView, ApplyJobApiView, already_applied_api_view

router = DefaultRouter()
router.register("jobs", JobViewSet)

urlpatterns = [
    path("search/", SearchApiView.as_view()),
    path("about-us", about_us),
    path("contact-us", contact_us),
    path("apply-job/<int:job_id>", ApplyJobApiView.as_view()),
    path("applied-jobs", AppliedJobsAPIView.as_view()),
    path("applied-for-job/<int:job_id>", already_applied_api_view),
]

urlpatterns += router.urls
