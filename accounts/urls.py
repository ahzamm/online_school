
from django.urls import path

from .views import UserRegisterationView

urlpatterns = [
    path('user-register/', UserRegisterationView.as_view(),
         name='User_Register'),

    path('user-login/', UserRegisterationView.as_view(),
         name='User_Login'),
]
