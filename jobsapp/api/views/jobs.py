from ..serializers import ContactSerializer, JobSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.reverse import reverse
from django_filters import rest_framework as filters
from ...models import JOB_INDEXES, Job, User
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from ..permissions import IsAuthorOrReadOnly
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from typing import Any

INDEXED_FILTERS = {field: ["contains", "exact"] for field in JOB_INDEXES}


class JobsViewList(ListCreateAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    # REVIEW: Which fields can be used to filter queries.
    # Here we use the same as the model indexes and can be extended
    filterset_fields = INDEXED_FILTERS

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        validated_data = request.data.copy()
        base_url = reverse("users-list")
        validated_data["user"] = f"{base_url}/{request.user.id}"
        serializer = self.get_serializer(data=validated_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(
                {"message": _("New job created."), "data": serializer.data},
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        return super().create(request, *args, **kwargs)


class JobsViewDetails(RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Job.objects.all()