from django.urls import path

from .views import fetch_practicals

urlpatterns = [
    path('fetchPracticals/', fetch_practicals),
]
