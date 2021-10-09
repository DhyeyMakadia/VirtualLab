from django.urls import path

from .views import fetch_practicals

urlpatterns = [
    path('fetch_practicals/', fetch_practicals),
]
