from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
    # ========================Admin Panel===========================
    path('',login,name='login'),
    path('profile/',profile,name='profile'),
    path('changepassword/',changepassword,name='changepassword'),
    path('register_admin/',register_admin,name='register_admin'),
    path('view_admin/',view_admin,name='view_admin'),
    path('update_admin/<int:id>',update_admin,name='update_admin'),
    path('delete_admin/<int:id>',delete_admin,name='delete_admin'),
    path('logout/',logout,name='logout'),














    # ========================Application===========================
    path('login/', obtain_auth_token),
    path('register/', registration),
    path('fetchUserApproval/', fetch_user_approval),
    path('fetchUserInfo/', fetch_user_info),
    path('rest_auth/', include('rest_auth.urls')),
]
