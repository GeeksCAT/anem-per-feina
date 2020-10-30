from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from ...models import JOB_INDEXES, Job, User


class UsersViewsList(ListAPIView):
    serializer_class = User
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class UsersViewDetails(CreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = User
    queryset = User.objects.all()
    print(queryset)
    permission_classes = [AllowAny]
