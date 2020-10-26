from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from django.db.models.query import QuerySet

from ...models import Job
from ..serializers import JobSerializer


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


@api_view(["GET"])
@permission_classes(
    [
        AllowAny,
    ]
)
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
