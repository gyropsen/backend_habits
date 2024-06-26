from rest_framework import generics
from rest_framework.permissions import AllowAny

from users import serializers


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        new_user = serializer.save(is_active=True)
        new_user.set_password(new_user.password)
        super().perform_create(new_user)
