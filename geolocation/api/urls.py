from django.urls import path

from .views import JobsGIS

urlpatterns = [
    path("geogis", JobsGIS.as_view(), name="jobs-map"),
]
