from os import name
from django.urls import path
from .views import *

urlpatterns = [
    # --------------------------Practical---------------------------
    path('view_practical/<int:id>',view_practical,name='view_practical'),
    path('add_practical/<int:id>',add_practical,name='add_practical'),
    path('update_practical/<int:id>',update_practical,name='update_practical'),
    path('delete_practical/<int:id>',delete_practical,name='delete_practical'),

    # -----------------------Practical-Details-----------------------
    path('view_practical_details/<int:id>',view_practical_details,name='view_practical_details'),
    # path('add_practical_details/<int:id>',add_practical_details,name='add_practical_details'),
    # path('update_practical_details/<int:id>',update_practical_details,name='update_practical_details'),
    # path('delete_practical_details/<int:id>',delete_practical_details,name='delete_practical_details'),

    path('add_youtube_links/<int:id>',add_youtube_links,name='add_youtube_links'),
    path('update_youtube_links/<int:id>',update_youtube_links,name='update_youtube_links'),
    path('delete_youtube_links/<int:id>',delete_youtube_links,name='delete_youtube_links'),
]
