from typing import Any

from rest_framework import status, viewsets
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from django.db.models.query import QuerySet
from django.utils.translation import ugettext as _

from ...models import Job
from ...utils import contact_us_email
from ..serializers import ContactSerializer, JobSerializer


class JobViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobSerializer
    queryset = serializer_class.Meta.model.objects.filter(filled=False)
    permission_classes = [AllowAny]


class SearchApiView(ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [AllowAny]

    def get_queryset(self) -> "QuerySet[Job]":
        if "location" in self.request.GET and "position" in self.request.GET:
            return self.serializer_class.Meta.model.objects.filter(
                filled=False,
                location__contains=self.request.GET["location"],
                title__contains=self.request.GET["position"],
            )
        else:
            return self.serializer_class.Meta.model.objects.filter(filled=False)


class ContactUs(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ContactSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            contact_us_email(serializer.validated_data)
            return Response(
                {"message": _("Email sent successfully.")}, status=status.HTTP_202_ACCEPTED
            )
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
