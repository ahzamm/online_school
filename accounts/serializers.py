from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (DjangoUnicodeDecodeError, force_bytes,
                                   smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from accounts.utils import Util
from accounts.models import Admin, Student, Teacher, User


class AdminRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Admin
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
        return Admin.objects.create_user(**validated_data)


class TeacherRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Teacher
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
        return Teacher.objects.create_user(**validated_data)


class StudentRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Student
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
        return Student.objects.create_user(**validated_data)


class AdminLoginSerializer(serializers.ModelSerializer):
    # serializer only see that we are sending post request so it throw "email is
    # already register" thats why we have to initilize extra email field
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = Admin
        fields = ['email', 'password']


class TeacherLoginSerializer(serializers.ModelSerializer):
    # serializer only see that we are sending post request so it throw "email is
    # already register" thats why we have to initilize extra email field
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = Teacher
        fields = ['email', 'password']


class StudentLoginSerializer(serializers.ModelSerializer):
    # serializer only see that we are sending post request so it throw "email is
    # already register" thats why we have to initilize extra email field
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = Student
        fields = ['email', 'password']


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'email', 'name']


class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'email', 'name']


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'email', 'name']


class AdminChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        old_password = data.get('old_password')
        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")
        user = self.context.get('user')
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                "Wrong old Password")
        user.set_password(password)
        user.save()
        return data


class TeacherChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        old_password = data.get('old_password')
        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")
        user = self.context.get('user')
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                "Wrong old Password")
        user.set_password(password)
        user.save()
        return data


class StudentChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        old_password = data.get('old_password')
        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")
        user = self.context.get('user')
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                "Wrong old Password")
        user.set_password(password)
        user.save()
        return data


class AdminChangeTeacherStudentPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        password2 = data.get('password2')

        user = User.objects.filter(email=email).first()
        if user is None:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")

        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")

        user.set_password(password)
        user.save()
        return data


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate(self, data):
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("===>", uid)
            token = PasswordResetTokenGenerator().make_token(user=user)
            print("====>", token)
            link = f"http://localhost:8000/api/reset/{uid}/{token}"
            print("====>", link)
            body = 'Click Following Link to Reset Your Password '+link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email
            }
            Util.send_email(data)
            return data
        else:
            raise serializers.ValidationError(
                "User with this email doesnot exist")


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError(
                    "Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(
                    'Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')
