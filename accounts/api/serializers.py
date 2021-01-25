from typing import Any, Dict, Optional, Union

from rest_framework import serializers

from django.utils.translation import ugettext as _

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "user_permissions",
            "groups",
            "is_staff",
            "is_active",
            "is_superuser",
            "last_login",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True, label=_("Confirm password")
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password2",
            "gender",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: Dict[str, Any]) -> User:
        email = validated_data["email"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        gender = validated_data["gender"]
        if email and User.objects.filter(email=email).exists():  # type: ignore
            raise serializers.ValidationError({"email": _("Email addresses must be unique.")})
        if password != password2:
            raise serializers.ValidationError({"password": _("The two passwords differ.")})
        user = User(email=email, gender=gender)
        user.set_password(password)
        user.save()
        return user
