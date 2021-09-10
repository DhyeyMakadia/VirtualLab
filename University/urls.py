from django.urls import path

from University.views import fetch_universities, fetch_institutes, fetch_departments, fetch_courses

urlpatterns = [
    path('university_list/', fetch_universities),
    path('institutes_list/', fetch_institutes),
    path('departments_list/', fetch_departments),
    path('courses_list/', fetch_courses),
]
