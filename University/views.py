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

# --------------------------------University-----------------------------------
# --------------------------------Courses-----------------------------------
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

# --------------------------------Institute-----------------------------------
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

# --------------------------------Department-----------------------------------

def view_department(request,id):
    err = ''
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        department = TblDepartments.objects.filter(institute_id=id)
        parent_institute = TblInstitutes.objects.get(id = id)

        return render(request, 'department.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err,'department':department,'parent_institute':parent_institute})
    else:
        return redirect('login')

def add_department(request,id):
    err = ''
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        parent_institute = TblInstitutes.objects.get(id = id)

        # PERMISSION TO INSERT
        if not User_Permissions.can_insert:
            return redirect('view_department',id=parent_institute.id)

        if request.POST:
            dept1 = request.POST['dept1']
            contactperson1 = request.POST['person1']
            cno1 = request.POST['cno1']

            Add_Department = TblDepartments()
            Add_Department.institute_id = parent_institute
            Add_Department.department_name = dept1
            Add_Department.department_contact_person = contactperson1
            Add_Department.department_contact = cno1
            Add_Department.save()
            return redirect('view_department',id=parent_institute.id)

        return render(request, 'add_department.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err,'parent_institute':parent_institute})
    else:
        return redirect('login')

def update_department(request,id):
    err = ''
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        Update_Department = TblDepartments.objects.get(id = id)
        parent_institute = Update_Department.institute_id

        # PERMISSION TO UPDATE
        if not User_Permissions.can_edit:
            return redirect('view_department',id=parent_institute.id)

        if request.POST:
            dept1 = request.POST['dept1']
            contactperson1 = request.POST['person1']
            cno1 = request.POST['cno1']

            Update_Department.department_name = dept1
            Update_Department.department_contact_person = contactperson1
            Update_Department.department_contact = cno1
            Update_Department.save()
            return redirect('view_department',id=parent_institute.id)

        return render(request, 'update_department.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err,'update_department':Update_Department,'parent_institute':parent_institute})
    else:
        return redirect('login')

def delete_department(request,id):
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        Del_Department = TblDepartments.objects.get(id = id)
        parent_institute = Del_Department.institute_id

        # PERMISSION TO DELETE
        if not User_Permissions.can_delete:
            return redirect('view_department',id = parent_institute.id)
        else:
            Del_Department.delete()
            return redirect('view_department',id = parent_institute.id)
    else:
        return redirect('login')
