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

    # ------------------------Youtube-Links---------------------------
    path('add_youtube_links/<int:id>',add_youtube_links,name='add_youtube_links'),
    path('update_youtube_links/<int:id>',update_youtube_links,name='update_youtube_links'),
    path('delete_youtube_links/<int:id>',delete_youtube_links,name='delete_youtube_links'),

    # ---------------------------Materials---------------------------
    path('add_materials/<int:id>',add_materials,name='add_materials'),
    path('update_materials/<int:id>',update_materials,name='update_materials'),
    path('delete_materials/<int:id>',delete_materials,name='delete_materials'),
]
