from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.messages import (
    PASSWORD_RESET_EMAIL_MESSAGE,
    PASSWORD_RESET_EMAIL_STATUS,
    PASSWORD_RESET_SUCCESS_MESSAGE,
    PASSWORD_RESET_SUCCESS_STATUS,
)
from accounts.serializers import (
    SendPasswordResetEmailSerializer,
    UserPasswordResetSerializer,
)


class SendPasswordResetEmailView(APIView):
    def post(self, request):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"msg": PASSWORD_RESET_EMAIL_MESSAGE},
            status=PASSWORD_RESET_EMAIL_STATUS,
        )


class UserPasswordResetView(APIView):
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data,
            context={"uid": uid, "token": token},
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            {"msg": PASSWORD_RESET_SUCCESS_MESSAGE},
            status=PASSWORD_RESET_SUCCESS_STATUS,
        )
