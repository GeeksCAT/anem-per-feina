from django.urls import path

from .views import JobsGIS

urlpatterns = [
    path("map", JobsGIS.as_view(), name="jobs-map"),
]
