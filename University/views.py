from django.shortcuts import render, redirect
from User.views import *
from User.models import *

from University.models import TblUniversity, TblInstitutes, TblDepartments, TblCourses
from University.serializers import TblUniversitySerializer, TblInstitutesSerializer, TblDepartmentsSerializer, TblCoursesSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.

# ========================= Admin Panel views ==============================
def dashboard(request):
    err = ''
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()

        return render(request, 'dashboard.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err})
    else:
        return redirect('login')

def add_university(request):
    err = ''
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()

        # PERMISSION TO INSERT
        if not User_Permissions.can_insert:
            return redirect('dashboard')

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

        return render(request, 'add_university.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err})
    else:
        return redirect('login')

def update_university(request,id):
    err = ''
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        Update_Univ = TblUniversity.objects.get(id = id)

        # PERMISSION TO UPDATE
        if not User_Permissions.can_edit:
            return redirect('dashboard')

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
            Update_Univ.save()
            return redirect('dashboard')

        return render(request, 'update_university.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err,'Update_Univ':Update_Univ})
    else:
        return redirect('login')

def delete_university(request,id):
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)

        # PERMISSION TO DELETE
        if not User_Permissions.can_delete:
            return redirect('dashboard')
        else:
            Del_Univ = TblUniversity.objects.get(id = id)
            Del_Univ.delete()
            return redirect('dashboard')
    else:
        return redirect('login')

def view_institute(request,id):
    err = ''
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        institute = TblInstitutes.objects.filter(university_id=id)
        parent_univ = TblUniversity.objects.get(id = id)

        return render(request, 'institute.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err,'institute':institute,'parent_univ':parent_univ})
    else:
        return redirect('login')

def add_institute(request,id):
    err = ''
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        parent_univ = TblUniversity.objects.get(id = id)

        # PERMISSION TO INSERT
        if not User_Permissions.can_insert:
            return redirect('view_institute',id=parent_univ.id)

        if request.POST:
            institute1 = request.POST['institute1']
            code1 = request.POST['code1']
            add1 = request.POST['add1']
            city = request.POST['city1']
            state = request.POST['state1']

            Add_Institute = TblInstitutes()
            Add_Institute.university_id = parent_univ
            Add_Institute.institute_name = institute1
            Add_Institute.institute_code = code1
            Add_Institute.institute_address = add1
            Add_Institute.institute_city = city
            Add_Institute.institute_state = state
            Add_Institute.save()
            return redirect('view_institute',id=parent_univ.id)

        return render(request, 'add_institute.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err,'parent_univ':parent_univ})
    else:
        return redirect('login')

def update_institute(request,id):
    err = ''
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        Update_Institute = TblInstitutes.objects.get(id = id)
        parent_univ = Update_Institute.university_id

        # PERMISSION TO UPDATE
        if not User_Permissions.can_edit:
            return redirect('view_institute',id=parent_univ.id)

        if request.POST:
            institute1 = request.POST['institute1']
            code1 = request.POST['code1']
            add1 = request.POST['add1']
            city = request.POST['city1']
            state = request.POST['state1']

            Update_Institute.institute_name = institute1
            Update_Institute.institute_code = code1
            Update_Institute.institute_address = add1
            Update_Institute.institute_city = city
            Update_Institute.institute_state = state
            Update_Institute.save()
            return redirect('view_institute',id=parent_univ.id)

        return render(request, 'update_institute.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err,'update_institute':Update_Institute,'parent_univ':parent_univ})
    else:
        return redirect('login')

def delete_institute(request,id):
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        Del_Institute = TblInstitutes.objects.get(id = id)
        parent_univ = Del_Institute.university_id

        # PERMISSION TO DELETE
        if not User_Permissions.can_delete:
            return redirect('view_institute',id = parent_univ.id)
        else:
            Del_Institute.delete()
            return redirect('view_institute',id = parent_univ.id)
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_educational_info(request):
    account = request.user
    user = TblUsers.objects.get(account_id=account)
    dic = {
        'university_id': user.institute_id.university_id.id,
        'institute_id': user.institute_id.id,
        'department_id': user.department_id.id,
    }
    return Response(dic)
