from os import name
from django.urls import path
from .views import *

urlpatterns = [
    # ------------------------Practical---------------------------
    path('view_practical/<int:id>',view_practical,name='view_practical'),
    path('add_practical/<int:id>',add_practical,name='add_practical'),
    path('update_practical/<int:id>',update_practical,name='update_practical'),
    path('delete_practical/<int:id>',delete_practical,name='delete_practical'),

    # ------------------------Practical-Details-----------------------
    path('view_practical_details/<int:id>',view_practical_details,name='view_practical_details'),

    # ------------------------Input-Parameters---------------------------
    path('add_input_parameters/<int:id>',add_input_parameters,name='add_input_parameters'),
    path('update_input_parameters/<int:id>',update_input_parameters,name='update_input_parameters'),
    path('delete_input_parameters/<int:id>',delete_input_parameters,name='delete_input_parameters'),

    # ------------------------Fixed-Input-Parameters---------------------------
    path('add_fixed_input_parameters/<int:id>',add_fixed_input_parameters,name='add_fixed_input_parameters'),
    path('update_fixed_input_parameters/<int:id>',update_fixed_input_parameters,name='update_fixed_input_parameters'),
    path('delete_fixed_input_parameters/<int:id>',delete_fixed_input_parameters,name='delete_fixed_input_parameters'),

    # ------------------------Output-Parameters---------------------------
    path('add_output_parameters/<int:id>',add_output_parameters,name='add_output_parameters'),
    path('update_output_parameters/<int:id>',update_output_parameters,name='update_output_parameters'),
    path('delete_output_parameters/<int:id>',delete_output_parameters,name='delete_output_parameters'),

    # ------------------------Fixed-Output-Parameters---------------------------
    path('add_fixed_output_parameters/<int:id>',add_fixed_output_parameters,name='add_fixed_output_parameters'),
    path('update_fixed_output_parameters/<int:id>',update_fixed_output_parameters,name='update_fixed_output_parameters'),
    path('delete_fixed_output_parameters/<int:id>',delete_fixed_output_parameters,name='delete_fixed_output_parameters'),

    # ------------------------Youtube-Links---------------------------
    path('add_youtube_links/<int:id>',add_youtube_links,name='add_youtube_links'),
    path('update_youtube_links/<int:id>',update_youtube_links,name='update_youtube_links'),
    path('delete_youtube_links/<int:id>',delete_youtube_links,name='delete_youtube_links'),

    # ------------------------Materials---------------------------
    path('add_materials/<int:id>',add_materials,name='add_materials'),
    path('update_materials/<int:id>',update_materials,name='update_materials'),
    path('delete_materials/<int:id>',delete_materials,name='delete_materials'),

    # ------------------------Images---------------------------
    path('add_multiple_images/<int:id>',add_multiple_images,name='add_multiple_images'),
    path('update_multiple_images/<int:id>',update_multiple_images,name='update_multiple_images'),
    path('update_images/<int:id>',update_images,name='update_images'),
    path('delete_images/<int:id>',delete_images,name='delete_images'),
]
