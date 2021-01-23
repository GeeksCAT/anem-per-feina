from typing import Any

from rest_framework import permissions, request, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import Address


class JobsGIS(ListAPIView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Address.objects.geojson()

    def get(self, request: request, *args: Any, **kwargs: Any) -> Response:
        # super().get(request, *args, **kwargs)
        return Response(self.get_queryset(), status=status.HTTP_200_OK)
