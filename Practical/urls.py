from django.urls import path
from .views import *

urlpatterns = [
    # --------------------------Practical---------------------------
    path('view_practical/<int:id>',view_practical,name='view_practical'),
    path('add_practical/<int:id>',add_practical,name='add_practical'),
    path('update_practical/<int:id>',update_practical,name='update_practical'),
    path('delete_practical/<int:id>',delete_practical,name='delete_practical'),
]
