from typing import Any

from rest_framework import status, views, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from django.core.mail import send_mail
from django.db.models.query import QuerySet

from ...models import Job
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


class ContactView(CreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            email_from = data.get("email")
            subject = data.get("subject")
            message = data.get("message")
            # TODO: Send email as background task with celery
            send_mail(
                subject,
                message,
                email_from,
                ["send to email"],
            )
            return Response(
                {"message": "Email sent successfully."}, status=status.HTTP_202_ACCEPTED
            )
        return Response(
            {"message": "Invalid data, please try it again."}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def about_us(request: Request) -> Response:
    # TODO: Get data from database
    content = {
        "name": "Anem per feina",
        "web_page": "",
        "email": "",
        "contact_phone": "",
        "location": "Girona, Catalunya",
        "lead_description": "",
        "text_description": "",
    }
    return Response(data=content, status=status.HTTP_200_OK)
