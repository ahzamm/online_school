from accounts.messages import (
    PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH,
    WRONG_OLD_PASSWORD,
)
from accounts.models import Student
from rest_framework import serializers


class StudentRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
    )
    roll_no = serializers.CharField(max_length=20)

    class Meta:
        model = Student
        fields = ["email", "name", "roll_no", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        password = data.get("password")
        password2 = data.get("password2")

        if password != password2:
            raise serializers.ValidationError(
                PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH,
            )

        return data

    def create(self, validated_data):
        return Student.objects.create_user(**validated_data)


class StudentLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = Student
        fields = ["email", "password"]


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "email", "name"]


class StudentChangePasswordSerializer(serializers.Serializer):
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
                PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH,
            )

        user = self.context.get("user")

        if not user.check_password(old_password):
            raise serializers.ValidationError(WRONG_OLD_PASSWORD)

        user.set_password(password)
        user.save()

        return data
