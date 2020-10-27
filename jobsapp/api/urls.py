from rest_framework.routers import DefaultRouter

from django.urls import path

from .views.common import JobViewSet, SearchApiView

router = DefaultRouter()
router.register("jobs", JobViewSet)

urlpatterns = [
    path("search/", SearchApiView.as_view()),
]

urlpatterns += router.urls
