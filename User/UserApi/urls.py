from django.urls import path, include
from .views import registration, fetch_user_approval, fetch_user_info

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login/', obtain_auth_token),
    path('register/', registration),
    path('fetchUserApproval/', fetch_user_approval),
    path('fetchUserInfo/', fetch_user_info),
    path('rest_auth/', include('rest_auth.urls')),
]
