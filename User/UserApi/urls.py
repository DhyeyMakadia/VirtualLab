from django.urls import path
from .views import registration, fetch_user_approval, fetch_user_info

urlpatterns = [
    path('register/', registration),
    path('fetchUserApproval/', fetch_user_approval),
    path('fetchUserInfo/', fetch_user_info),
]
