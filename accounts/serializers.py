from rest_framework import serializers
from accounts.models import Student, Teacher, User


class UserRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")
        return data

    def create(self, validated_data):
        return User.objects.create_superuser(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
