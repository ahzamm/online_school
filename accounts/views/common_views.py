
from accounts.messages import *
from accounts.serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView


class SendPasswordResetEmailView(APIView):
    def post(self, request):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"msg": PASSWORD_RESET_EMAIL_MESSAGE},
                        status=PASSWORD_RESET_EMAIL_STATUS)


class UserPasswordResetView(APIView):
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data,
                                                 context={'uid': uid,
                                                          'token': token})
        serializer.is_valid(raise_exception=True)

        return Response({'msg': PASSWORD_RESET_SUCCESS_MESSAGE},
                        status=PASSWORD_RESET_SUCCESS_STATUS)
