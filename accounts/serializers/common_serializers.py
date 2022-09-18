
from accounts.messages import *
from accounts.models import User
from accounts.utils import Util
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (DjangoUnicodeDecodeError, force_bytes,
                                   smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate(self, data):
        email = data.get('email')

        # If the user with the provided email doesnot exists,
        # error will be generated
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(USER_WITH_EMAIL_DOESNT_EXIST)

        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user=user)
        link = password_reset_link(uid, token)
        body = PASSWORD_RESET_EMAIL_BODY + link
        data = {
            'subject': PASSWORD_RESET_EMAIL_SUBJECT,
            'body': body,
            'to_email': user.email
        }
        Util.send_email(data)

        return data


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,
                                     style={'input_type': 'password'},
                                     write_only=True)

    password2 = serializers.CharField(max_length=255,
                                      style={'input_type': 'password'},
                                      write_only=True)

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')

            if password != password2:
                raise serializers.ValidationError(
                    PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH)

            _id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(
                    'Token is not Valid or Expired')

            user.set_password(password)
            user.save()

            return attrs

        except DjangoUnicodeDecodeError as e:
            PasswordResetTokenGenerator().check_token(user, token)

            raise serializers.ValidationError(
                'Token is not Valid or Expired') from e
