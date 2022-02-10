from django.urls import path, re_path
from .views import *

urlpatterns = [
    # ========================Admin Panel===========================
    path('',login_page,name='login'),
    path('profile/',profile,name='profile'),
    path('changepassword/',changepassword,name='changepassword'),
    path('register_admin/',register_admin,name='register_admin'),
    path('view_admin/',view_admin,name='view_admin'),
    path('update_admin/<int:id>',update_admin,name='update_admin'),
    path('delete_admin/<int:id>',delete_admin,name='delete_admin'),
    path('logout/',logout_page,name='logout'),
    path('sel_institute/',sel_institute,name='sel_institute'),
    path('sel_department/',sel_department,name='sel_department'),
    path('sel_courses/',sel_courses,name='sel_courses'),
    path('update_institute/',update_institute,name='update_institute'),
    path('update_department/',update_department,name='update_department'),
    path('update_courses/',update_courses,name='update_courses'),

    path('view_requests/',view_requests,name='view_requests'),
    path('approve_student/<int:id>',approve_student,name='approve_student'),
    path('decline_student/<int:id>', decline_student, name='decline_student'),
    path('view_accepted_students/',view_accepted_students,name='view_accepted_students'),
    path('p1/', print_permissions),
]

