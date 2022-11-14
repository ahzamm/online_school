from accounts.custom_permissions import IsAdmin
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from swagger_responses.classes_responses.classes_responses import (
    timetable_register_response,
)

from ..messages import (
    TIMETABLE_REGISTER_SUCCESS_MESSAGE,
    TIMETABLE_REGISTER_SUCCESS_STATUS,
)
from ..serializer import TimeTableSerializer


class AdminCreateTimeTableView(GenericAPIView):
    """### For Admin to create new Timetable"""

    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = TimeTableSerializer

    @swagger_auto_schema(responses=timetable_register_response)
    def post(self, request):
        serializer = TimeTableSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"msg": TIMETABLE_REGISTER_SUCCESS_MESSAGE},
            status=TIMETABLE_REGISTER_SUCCESS_STATUS,
        )
