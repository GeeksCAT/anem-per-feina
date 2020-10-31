from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from ...models import User
from ..permissions import IsSelfOrReadOnly, AllowAny
from ..serializers import UserSerializer


class UsersViewsList(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class UsersViewDetails(CreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    print(queryset)
    permission_classes = [IsSelfOrReadOnly]
