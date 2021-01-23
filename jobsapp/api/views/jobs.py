from typing import Any

from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse

from ...models import JOB_INDEXES, Job, User
from ..permissions import IsAuthorOrReadOnly
from ..serializers import ContactSerializer, JobSerializer, UserSerializer

INDEXED_FILTERS = {field: ["contains", "exact"] for field in JOB_INDEXES}


class JobsViewList(ListCreateAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    # REVIEW: Which fields can be used to filter queries.
    # Here we use the same as the model indexes and can be extended
    filterset_fields = INDEXED_FILTERS

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JobsViewDetails(RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Job.objects.all()
