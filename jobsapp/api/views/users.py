from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ...models import User
from ..serializers import UserSerializer


class UsersViewsList(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class UsersViewDetails(CreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    print(queryset)
    permission_classes = [IsAuthenticatedOrReadOnly]
