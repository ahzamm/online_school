

from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import UserRegisterationSerializer


class UserRegisterationView(APIView):
    def post(self, request):
        serializer = UserRegisterationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Registeration Success'}, status=201)


class UserLoginView(APIView):
    def post(self, request):
        return Response({'msg': 'Login Success'}, status=200)
