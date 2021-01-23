from django.urls import path

from .views import JobsMap

urlpatterns = [path("map", JobsMap.as_view(), name="map")]
