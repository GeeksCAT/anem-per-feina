from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from ..permissions import IsSelfOrReadOnly

from ...models import User
from ..serializers import UserSerializer


class UsersViewsList(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsSelfOrReadOnly]


class UsersViewDetails(CreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    print(queryset)
    permission_classes = [IsSelfOrReadOnly]
