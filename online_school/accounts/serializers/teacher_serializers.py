from rest_framework import serializers

from accounts.messages import (
    PASSWORD_CONFIRM_PASSWORD_NOT_MATCH,
    WRONG_OLD_PASSWORD,
)
from accounts.models import Teacher


class TeacherRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
    )

    class Meta:
        model = Teacher
        fields = ["email", "name", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        password = data.get("password")
        password2 = data.get("password2")

        if password == password2:
            return data

        raise serializers.ValidationError(
            PASSWORD_CONFIRM_PASSWORD_NOT_MATCH,
        )

    def create(self, validated_data):
        return Teacher.objects.create_user(**validated_data)


class TeacherLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = Teacher
        fields = ["email", "password"]


class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["id", "email", "name"]


class TeacherChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
    )

    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
    )

    password2 = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
    )

    def validate(self, data):
        old_password = data.get("old_password")
        password = data.get("password")
        password2 = data.get("password2")

        if password != password2:
            raise serializers.ValidationError(
                PASSWORD_CONFIRM_PASSWORD_NOT_MATCH,
            )

        user = self.context.get("user")

        if not user.check_password(old_password):
            raise serializers.ValidationError(WRONG_OLD_PASSWORD)

        user.set_password(password)
        user.save()

        return data
