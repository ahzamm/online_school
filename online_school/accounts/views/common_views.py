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
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from swagger_responses.accounts_responses.common_responses import (
    password_reset_response,
    send_password_reset_email_response,
)


class SendPasswordResetEmailView(GenericAPIView):
    """## For User to recieve **`password reset email` to the provided email**"""

    serializer_class = SendPasswordResetEmailSerializer

    @swagger_auto_schema(responses=send_password_reset_email_response)
    def post(self, request):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"msg": PASSWORD_RESET_EMAIL_MESSAGE},
            status=PASSWORD_RESET_EMAIL_STATUS,
        )


class UserPasswordResetView(GenericAPIView):
    """## For User to **`reset password`** of the account"""

    serializer_class = UserPasswordResetSerializer

    @swagger_auto_schema(responses=password_reset_response)
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
