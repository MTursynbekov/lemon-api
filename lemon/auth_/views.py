from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from auth_ import serializers
from auth_.models import MainUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = MainUser.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.UserCreateSerializer
        return self.serializer_class
