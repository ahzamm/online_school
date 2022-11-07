from rest_framework import serializers

from accounts.messages import (
    NO_STUDENT_TEACHER_WITH_EMAIL,
    PASSWORD_CONFIRM_PASSWORD_NOT_MATCH,
    WRONG_OLD_PASSWORD,
)
from accounts.models import Admin, User


class AdminRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
    )

    class Meta:
        model = Admin
        fields = ["email", "name", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        password = data.get("password")
        password2 = data.get("password2")

        if password != password2:
            raise serializers.ValidationError(
                PASSWORD_CONFIRM_PASSWORD_NOT_MATCH,
            )

        return data

    def create(self, validated_data):
        return Admin.objects.create_user(**validated_data)


class AdminLoginSerializer(serializers.ModelSerializer):
    # serializer only see that we are sending post request so it throw "email
    # is already register" thats why we have to initilize extra email field
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = Admin
        fields = ["email", "password"]


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ["id", "email", "name"]


class AdminChangePasswordSerializer(serializers.Serializer):
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


class AdminChangeTeacherStudentPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
    )

    password2 = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
    )

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        password2 = data.get("password2")

        user = User.objects.filter(email=email).first()

        if user is None:
            raise serializers.ValidationError(NO_STUDENT_TEACHER_WITH_EMAIL)

        if password != password2:
            raise serializers.ValidationError(
                PASSWORD_CONFIRM_PASSWORD_NOT_MATCH,
            )

        user.set_password(password)
        user.save()

        return data
