from django.shortcuts import render, redirect
from User.views import *
from User.models import *

from University.models import TblUniversity, TblInstitutes, TblDepartments, TblCourses
from University.serializers import TblUniversitySerializer, TblInstitutesSerializer, TblDepartmentsSerializer, TblCoursesSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

# ========================= Admin Panel views ==============================
def dashboard(request):
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        univ = TblUniversity.objects.all()
        return render(request, 'dashboard.html', {'Users': User,'admin':User_Admin,'univ':univ})
    else:
        return redirect('login')

def add_university(request):
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        univ = TblUniversity.objects.all()
        if request.POST:
            univ1 = request.POST['univ1']
            unique_no = request.POST['uno1']
            add1 = request.POST['add1']
            city = request.POST['city1']
            state = request.POST['state1']

            Add_Univ = TblUniversity()
            Add_Univ.university_name = univ1
            Add_Univ.university_unique_num =unique_no
            Add_Univ.university_address = add1
            Add_Univ.university_city = city
            Add_Univ.university_state = state
            Add_Univ.save()
            return redirect('dashboard')

        return render(request, 'add_university.html', {'Users': User,'admin':User_Admin,'univ':univ})
    else:
        return redirect('login')

def update_university(request,id):
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        univ = TblUniversity.objects.all()
        Update_Univ = TblUniversity.objects.get(id = id)
        if request.POST:
            univ1 = request.POST['univ1']
            unique_no = request.POST['uno1']
            add1 = request.POST['add1']
            city = request.POST['city1']
            state = request.POST['state1']

            Update_Univ.university_name = univ1
            Update_Univ.university_unique_num = unique_no
            Update_Univ.university_address = add1
            Update_Univ.university_city = city
            Update_Univ.university_state = state
            # Update_Univ.update_date_time = True
            Update_Univ.save()
            return redirect('dashboard')
        return render(request, 'update_university.html', {'Users': User,'admin':User_Admin,'univ':univ,'Update_Univ':Update_Univ})
    else:
        return redirect('login')

def delete_university(request,id):
    if 'admin_session' in request.session.keys():
        Del_Univ = TblUniversity.objects.get(id = id)
        Del_Univ.delete()
        return redirect('dashboard')
    else:
        return redirect('login')
# ========================= rest api views ==============================

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
