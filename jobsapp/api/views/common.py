from typing import Any

from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.contrib.flatpages.models import FlatPage
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _

from ...models import Job, User
from ...utils import contact_us_email
from ..permissions import IsAuthorOrReadOnly
from ..serializers import ContactSerializer, JobSerializer, UserSerializer


class JobsViewList(ListCreateAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    # REVIEW: Which fields can be used to filter queries
    filterset_fields = {
        "category": ["contains", "exact"],
        "location": ["contains"],
        "title": ["contains"],
    }

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        validated_data = request.data.copy()
        base_url = reverse("users-list")
        validated_data["user"] = f"{base_url}/{request.user.id}"
        serializer = self.get_serializer(data=validated_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(
                {"message": "New job created.", "data": serializer.data},
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        return super().create(request, *args, **kwargs)


class JobsViewDetails(RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Job.objects.all()


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


class AboutUs(ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        about_content = FlatPage.objects.filter(url="/about-us/").first()
        content = {
            "content": about_content.content,
        }
        return Response(data=content, status=status.HTTP_200_OK)


class UsersList(ListAPIView, RetrieveAPIView):
    serializer_class = User
    queryset = User.objects.all()
    permission_classes = [AllowAny]
