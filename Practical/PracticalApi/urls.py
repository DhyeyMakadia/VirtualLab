from django.urls import path

from .views import fetch_practicals, fetch_practical_values, fetch_youtube_links

urlpatterns = [
    path('fetchPracticals/', fetch_practicals),
    path('fetchPracticalValues/', fetch_practical_values),
    path('fetchYoutubeLinks/', fetch_youtube_links),
]
