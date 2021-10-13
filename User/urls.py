from django.urls import path
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

    path('view_requests/',view_requests,name='view_requests'),
    path('approve_student/<int:id>',approve_student,name='approve_student'),
    path('view_accepted_students/',view_accepted_students,name='view_accepted_students'),
]
