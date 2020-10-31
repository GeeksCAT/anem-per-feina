from typing import Any

from rest_framework import status, viewsets
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from django.utils.translation import ugettext as _
from rest_framework.response import Response

from django.contrib.flatpages.models import FlatPage

from ...utils import contact_us_email
from ..serializers import ContactSerializer, JobSerializer


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
