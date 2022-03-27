from django.urls import path
from .views import *

urlpatterns = [
    # --------------------------University---------------------------
    path('dashboard/', dashboard, name='dashboard'),
    path('add_university/', add_university, name='add_university'),
    path('update_university/<int:key>', update_university, name='update_university'),
    path('delete_university/<int:key>', delete_university, name='delete_university'),

    # --------------------------Institute---------------------------
    path('view_institute/<int:key>', view_institute, name='view_institute'),
    path('add_institute/<int:key>', add_institute, name='add_institute'),
    path('update_institute/<int:key>', update_institute, name='update_institute'),
    path('delete_institute/<int:key>', delete_institute, name='delete_institute'),

    # --------------------------Department---------------------------
    path('view_department/<int:key>', view_department, name='view_department'),
    path('add_department/<int:key>', add_department, name='add_department'),
    path('update_department/<int:key>', update_department, name='update_department'),
    path('delete_department/<int:key>', delete_department, name='delete_department'),

    # --------------------------Course---------------------------
    path('view_course/<int:key>', view_course, name='view_course'),
    path('add_course/<int:key>', add_course, name='add_course'),
    path('update_course/<int:key>', update_course, name='update_course'),
    path('delete_course/<int:key>', delete_course, name='delete_course'),
]
