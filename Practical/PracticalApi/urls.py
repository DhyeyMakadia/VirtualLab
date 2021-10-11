from django.urls import path

from .views import fetch_practicals, fetch_practical_values, fetch_youtube_links, fetch_practical_images, fetch_practical_materials

urlpatterns = [
    path('fetchPracticals/', fetch_practicals),
    path('fetchPracticalValues/', fetch_practical_values),
    path('fetchYoutubeLinks/', fetch_youtube_links),
    path('fetchPracticalImages/', fetch_practical_images),
    path('fetchPracticalMaterials/', fetch_practical_materials),
]
