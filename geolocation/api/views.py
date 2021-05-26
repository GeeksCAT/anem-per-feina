from typing import Any

from rest_framework import request, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import Map


class JobsMap(ListAPIView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Map.objects.geojson()

    def get(self, request: request, *args: Any, **kwargs: Any) -> Response:
        return Response(self.get_queryset(), status=status.HTTP_200_OK)
