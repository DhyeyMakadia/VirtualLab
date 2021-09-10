from django.shortcuts import render

from University.models import TblUniversity, TblInstitutes, TblDepartments, TblCourses
from University.serializers import TblUniversitySerializer, TblInstitutesSerializer, TblDepartmentsSerializer, TblCoursesSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.


# REST API View

@api_view(['GET'])
def fetch_universities(request):
    universities = TblUniversity.objects.all()
    serializer = TblUniversitySerializer(universities, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def fetch_institutes(request):
    institutes = TblInstitutes.objects.filter(university_id=request.GET['university_id'])
    if not institutes:
        return Response({'error': 101, 'message': 'No Institute found for university'})
    serializer = TblInstitutesSerializer(institutes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def fetch_departments(request):
    departments = TblDepartments.objects.filter(institute_id=request.GET['institute_id'])
    if not departments:
        return Response({'error': 102, 'message': 'No Departments found for Institute'})
    serializer = TblDepartmentsSerializer(departments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def fetch_courses(request):
    courses = TblCourses.objects.filter(department_id=request.GET['department_id'])
    if not courses:
        return Response({'error': 103, 'message': 'No Courses found for Department'})
    serializer = TblCoursesSerializer(courses, many=True)
    return Response(serializer.data)
