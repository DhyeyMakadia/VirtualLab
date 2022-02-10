from django.shortcuts import redirect, render
from University.views import *

# modules for rest api
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import RegistrationSerializer, TblUserSerializer


from University.models import TblDepartments
from User.models import *
from django.http import HttpResponseRedirect
# Create your views here.


# ========================= Admin Panel views ==============================

def login(request):
    err = str()
    if request.POST:
        em = request.POST['em1']
        pwd = request.POST['pass']

        try:
            obj = Account.objects.get(email=em)
            if obj.check_password(pwd):
                request.session['admin_session'] = obj.id
                return redirect('dashboard')
            else:
                err = 'Wrong Password'
        except:
            err = 'Wrong Email'
    return render(request,'login.html',{'error':err})

def profile(request):
    err = str()
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        if request.POST:
            nm = request.POST['nm1']
            cno = request.POST['cno1']
            prof1 = request.FILES.get('prof1')

            User_Admin.admin_name = nm
            User_Admin.admin_contact_number = cno
            if prof1 != None:
                User_Admin.admin_image = prof1
            User_Admin.save()
        return render(request,'profile.html',{'Users':User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err})
    else:
        return redirect('login')

def changepassword(request):
    err = suc = str()
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        if request.POST:
            pwd = request.POST['pwd']
            pwd1 = request.POST['pwd1']
            pwd2 = request.POST['pwd2']

            if User.check_password(pwd):
                if pwd1 == pwd2:
                    User.set_password(pwd1)
                    User.save()
                    suc = 'Password Changed Successfully'
                else:
                    err = 'Password Must Match !!'
            else:
                err = 'Wrong Password'

        return render(request,'changepassword.html',{'Users':User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err,'success':suc})
    else:
        return redirect('login')

def register_admin(request):
    err = str()
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()

        # PERMISSION TO INSERT(ONLY TO SUPERUSER)
        if not User.is_superuser:
            return redirect('view_admin')

        if request.POST:
            em = request.POST['em1']
            pwd = request.POST['pass1']
            nm = request.POST['nm1']
            role = request.POST['role1']
            cno = request.POST['cno1']
            prof1 = request.FILES.get('prof1')

            # ACCOUNT
            serializer = RegistrationSerializer(data={'email':em,'password':pwd,'password2':pwd,'is_admin':True},partial=True)
            if serializer.is_valid():
                account = serializer.save()
            else:
                err = "Invalid Input"

            # ADMIN
            obj_account = Account.objects.get(email = em)
            obj_account.is_admin = True
            obj_account.is_staff = True
            obj_account.save()
            New_Admin = TblAdmin()
            New_Admin.account_id = obj_account
            New_Admin.admin_name = nm
            New_Admin.admin_contact_number = cno
            if prof1 != None:
                New_Admin.admin_image = prof1
            New_Admin.save()

            # PERMISSIONS
            obj_admin = TblAdmin.objects.get(account_id=obj_account)
            New_Permissions = TblPermissions()
            New_Permissions.role = role
            New_Permissions.admin_id = obj_admin
            New_Permissions.save()

            permission_univ = request.POST.getlist('university')
            permission_institute = request.POST.getlist('institute')
            permission_department = request.POST.getlist('department')
            permission_courses = request.POST.getlist('courses')
            New_Permissions.allowed_university.set([int(x) for x in permission_univ])
            New_Permissions.allowed_institute.set([int(x) for x in permission_institute]) 
            New_Permissions.allowed_department.set([int(x) for x in permission_department])
            New_Permissions.allowed_courses.set([int(x) for x in permission_courses])
            New_Permissions.save()
            return redirect('view_admin')

        return render(request, 'register_admin.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err})
    else:
        return redirect('login')

def sel_institute(request):
    university_id = request.GET.getlist('univ_id[]')
    institutes = TblInstitutes.objects.filter(university_id__in = university_id)
    return render(request,'select_option.html',{'institutes':institutes})

def sel_department(request):
    institute_id = request.GET.getlist('institute_id[]')
    departments = TblDepartments.objects.filter(institute_id__in = institute_id)
    return render(request,'select_option.html',{'departments':departments})

def sel_courses(request):
    department_id = request.GET.getlist('department_id[]')
    courses = TblCourses.objects.filter(department_id__in = department_id)
    return render(request,'select_option.html',{'courses':courses})

def view_admin(request):
    err = str()
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        All_Admin = TblPermissions.objects.all()

        # PERMISSION TO VIEW
        if not User_Permissions.can_view:
            return redirect('dashboard')

        return render(request, 'view_admin.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err,'all_admin':All_Admin})
    else:
        return redirect('login')

def update_admin(request,id):
    err = str()
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        univ = TblUniversity.objects.all()
        institute = TblInstitutes.objects.all()
        department = TblDepartments.objects.all()
        courses = TblCourses.objects.all()
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        Update_Admin = TblAdmin.objects.get(id = id)
        Update_Permissions = TblPermissions.objects.get(admin_id = Update_Admin)

        # RESTRICTED TO UPDATE OWN PROFILE
        if User_Admin.id == id:
            return redirect('view_admin')

        # PERMISSION TO UPDATE
        if not User_Permissions.can_edit:
            return redirect('view_admin')

        if request.POST:
            nm = request.POST['nm1']
            cno = request.POST['cno1']
            prof1 = request.FILES.get('prof1')
            can_view = request.POST['can_view']
            can_insert = request.POST['can_insert']
            can_edit = request.POST['can_edit']
            can_delete = request.POST['can_delete']

            Update_Admin.admin_name = nm
            Update_Admin.admin_contact_number = cno
            if prof1 != None:
                Update_Admin.admin_image = prof1

            if can_view == "true":
                Update_Permissions.can_view = True
            elif can_view == "false":
                Update_Permissions.can_view = False

            if can_insert == "true":
                Update_Permissions.can_insert = True
            elif can_insert == "false":
                Update_Permissions.can_insert = False

            if can_edit == "true":
                Update_Permissions.can_edit = True
            elif can_edit == "false":
                Update_Permissions.can_edit = False

            if can_delete == "true":
                Update_Permissions.can_delete = True
            elif can_delete == "false":
                Update_Permissions.can_delete = False

            Update_Permissions.save()
            Update_Admin.save()
            return redirect('view_admin')

        return render(request, 'update_admin.html', {'Users': User,'admin':User_Admin,'univ':univ,'institute':institute,'department':department,'courses':courses,'permissions':User_Permissions,'update_admin':Update_Admin,'update_permissions':Update_Permissions,'error':err})
    else:
        return redirect('login')

def update_institute(request):
    university_id = request.GET.getlist('univ_id[]')
    institutes = TblInstitutes.objects.filter(university_id__in = university_id)
    return render(request,'update_option.html',{'institutes':institutes})

def update_department(request):
    institute_id = request.GET.getlist('institute_id[]')
    departments = TblDepartments.objects.filter(institute_id__in = institute_id)
    return render(request,'update_option.html',{'departments':departments})

def update_courses(request):
    department_id = request.GET.getlist('department_id[]')
    courses = TblCourses.objects.filter(department_id__in = department_id)
    return render(request,'update_option.html',{'courses':courses})

def delete_admin(request,id):
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)

        # CAN'T DELETE OWN PROFILE
        if User.id == id:
            return redirect('view_admin')
        
        # PERMISSION TO DELETE
        if not User_Permissions.can_delete:
            return redirect('view_admin')
        else:
            Del_Admin = Account.objects.get(id = id)
            Del_Admin.delete()
            return redirect('view_admin')
    else:
        return redirect('login')

def logout(request):
    if 'admin_session' in request.session.keys():
        del request.session['admin_session']
        return redirect('login')
    else:
        return redirect('login')

# ----------------------------For-Student----------------------------------
def view_requests(request):
    err = str()
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        New_Request = TblUsers.objects.filter(is_approved=False)

        # PERMISSION TO VIEW
        if not User_Permissions.can_view:
            return redirect('dashboard')

        return render(request, 'view_student_new_request.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err,'new_request':New_Request})
    else:
        return redirect('login')

def approve_student(request,id):
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        Student = TblUsers.objects.get(id=id)

        # PERMISSION TO UPDATE
        if not User_Permissions.can_edit:
            return redirect('dashboard')

        Student.is_approved = True
        Student.save()
        return redirect('view_requests')
    else:
        return redirect('login')

def decline_student(request,id):
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        
        # PERMISSION TO DELETE
        if not User_Permissions.can_delete:
            return redirect('view_requests')
        else:
            Del_Student = Account.objects.get(id = id)
            Del_Student.delete()
            return redirect('view_requests')
    else:
        return redirect('login')

def view_accepted_students(request):
    err = str()
    if 'admin_session' in request.session.keys():
        User = Account.objects.get(id=int(request.session['admin_session']))
        User_Admin = TblAdmin.objects.get(account_id=User)
        User_Permissions = TblPermissions.objects.get(admin_id = User_Admin)
        univ = TblUniversity.objects.all()
        Accepted_Students = TblUsers.objects.filter(is_approved=True)

        # PERMISSION TO VIEW
        if not User_Permissions.can_view:
            return redirect('dashboard')

        return render(request, 'view_accepted_students.html', {'Users': User,'admin':User_Admin,'univ':univ,'permissions':User_Permissions,'error':err,'accepted_students':Accepted_Students})
    else:
        return redirect('login')