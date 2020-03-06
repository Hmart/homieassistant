from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from . import models, permissions, serializers


class RegistrationView(generics.CreateAPIView):
    serializer_class = serializers.RegistrationSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)


class RestorePasswordView(generics.GenericAPIView):
    serializer_class = serializers.RestorePasswordSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["email"]
        user.send_password_restore_email()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RestorePasswordConfirmView(generics.UpdateAPIView):
    serializer_class = serializers.RestorePasswordConfirmSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get_object(self):
        return get_object_or_404(models.User, pk=self.kwargs["user_id"])


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserMeView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Removes the currently logged in user (requires field 'password')
    """

    serializer_class = serializers.UserMeSerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        perms = super().get_permissions()
        if self.request.method not in (
            "GET",
            "HEAD",
            "POST",
            "PUT",
            "PATCH",
            "OPTIONS",
        ):
            perms.append(permissions.PasswordPermission())
        return perms

    def get_object(self):
        return self.request.user
