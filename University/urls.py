from django.urls import path
from .views import *

urlpatterns = [
    # --------------------------University---------------------------
    path('dashboard/',dashboard,name='dashboard'),
    path('add_university/',add_university,name='add_university'),
    path('update_university/<int:id>',update_university,name='update_university'),
    path('delete_university/<int:id>',delete_university,name='delete_university'),

    # --------------------------Institute---------------------------
    path('view_institute/<int:id>',view_institute,name='view_institute'),
    path('add_institute/<int:id>',add_institute,name='add_institute'),
    path('update_institute/<int:id>',update_institute,name='update_institute'),
    path('delete_institute/<int:id>',delete_institute,name='delete_institute'),

    # --------------------------Department---------------------------
    path('view_department/<int:id>',view_department,name='view_department'),
    path('add_department/<int:id>',add_department,name='add_department'),
    path('update_department/<int:id>',update_department,name='update_department'),
    path('delete_department/<int:id>',delete_department,name='delete_department'),

    # --------------------------Course---------------------------
    path('view_course/<int:id>',view_course,name='view_course'),
    path('add_course/<int:id>',add_course,name='add_course'),
    path('update_course/<int:id>',update_course,name='update_course'),
    path('delete_course/<int:id>',delete_course,name='delete_course'),
]
