from django.urls import path

from .views import fetch_universities, fetch_institutes, fetch_departments, fetch_courses, fetch_educational_info

urlpatterns = [
    path('fetchUniversities/', fetch_universities),
    path('fetchInstitutes/', fetch_institutes),
    path('fetchDepartments/', fetch_departments),
    path('fetchCourses/', fetch_courses),
    path('fetchEducationalInfo/', fetch_educational_info),
]
