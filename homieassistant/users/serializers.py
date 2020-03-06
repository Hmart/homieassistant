from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from utils.fields import LowerCaseEmailField

from . import models


class RegistrationSerializer(serializers.ModelSerializer):
    email = LowerCaseEmailField(
        validators=[
            UniqueValidator(queryset=models.User.objects.all(), lookup="iexact")
        ]
    )
    password = serializers.CharField(
        validators=[validate_password],
        style={"input_type": "password"},
        write_only=True,
    )
    token = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
            "token",
        )

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)

    def get_token(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        return token.key


class RestorePasswordSerializer(serializers.Serializer):
    email = serializers.SlugRelatedField(
        slug_field="email__iexact", queryset=models.User.objects.all(), write_only=True,
    )


class RestorePasswordConfirmSerializer(serializers.ModelSerializer):
    INVALID_TOKEN_ERROR = "Invalid token"

    password = serializers.CharField(
        validators=[validate_password],
        style={"input_type": "password"},
        write_only=True,
    )
    token = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.User
        fields = ("password", "token")

    def validate_token(self, token):
        user = self.instance
        token_is_valid = default_token_generator.check_token(user, token)
        if not token_is_valid:
            raise serializers.ValidationError(self.INVALID_TOKEN_ERROR)

        return token

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    CURRENT_PASSWORD_INCORRECT_ERROR = "Current password was incorrect"

    current_password = serializers.CharField(
        label="Current password", source="password", write_only=True,
    )
    new_password = serializers.CharField(
        label="New password", validators=[validate_password], write_only=True,
    )

    class Meta:
        model = models.User
        fields = ("current_password", "new_password")

    def validate_current_password(self, current_password):
        if not self.context["request"].user.check_password(current_password):
            raise serializers.ValidationError(self.CURRENT_PASSWORD_INCORRECT_ERROR)
        return current_password

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_staff",
        )
        read_only_fields = (
            "id",
            "is_staff",
        )
