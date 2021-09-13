from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
    # ========================Admin Panel===========================
    path('',login,name='login'),
    path('profile/',profile,name='profile'),
    path('changepassword/',changepassword,name='changepassword'),
    path('logout/',logout,name='logout'),














    # ========================Application===========================
    path('login/', obtain_auth_token),
    path('register/', registration),
]
