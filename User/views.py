from django.contrib.auth.models import Permission
from django.shortcuts import redirect, render

from University.models import TblCourses, TblDepartments, TblInstitutes, TblUniversity

from .serializers import RegistrationSerializer

from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from User.models import Account, TblAdmin, TblPermissions, TblUsers
from .decorators import check_authentication


# from django.contrib.auth.decorators import permission_required
# from django.contrib.auth.models import Group

# Create your views here.


# ========================= Admin Panel views ==============================
def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            email = request.POST['em1']
            pwd = request.POST['pass']
            user = authenticate(request, username=email, password=pwd)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username OR password is incorrect')
                err = 'Username OR password is incorrect'
            return render(request, 'login.html', {'error': err})
        if request.method == 'GET':
            return render(request, 'login.html')


@check_authentication
def profile(request):
    err = str()
    User_Admin = TblAdmin.objects.get(account_id=request.user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
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
    return render(request, 'profile.html',
                  {'Users': request.user, 'admin': User_Admin, 'univ': univ, 'permissions': User_Permissions,
                   'error': err})


@check_authentication
def changepassword(request):
    err = suc = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    univ = TblUniversity.objects.all()
    if request.POST:
        pwd = request.POST['pwd']
        pwd1 = request.POST['pwd1']
        pwd2 = request.POST['pwd2']
        if user.check_password(pwd):
            if pwd1 == pwd2:
                user.set_password(pwd1)
                user.save()
                suc = 'Password Changed Successfully'
            else:
                err = 'Password Must Match !!'
        else:
            err = 'Wrong Password'
    return render(request, 'changepassword.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'permissions': User_Permissions, 'error': err,
                   'success': suc})


@check_authentication
def register_admin(request):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    univ = TblUniversity.objects.all()
    # PERMISSION TO INSERT(ONLY TO SUPERUSER)
    if not user.is_superuser:
        return redirect('view_admin')
    if request.POST:
        em = request.POST['em1']
        pwd = request.POST['pass1']
        nm = request.POST['nm1']
        role = request.POST['role1']
        cno = request.POST['cno1']
        prof1 = request.FILES.get('prof1')
        # ACCOUNT
        serializer = RegistrationSerializer(data={'email': em}, partial=True)
        if serializer.is_valid():
            account = serializer.save()
            account.set_password(pwd)
            account.is_admin = True
            account.save()
        else:
            err = "Invalid Input"
        # ADMIN
        obj_account = Account.objects.get(email=em)
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
        return redirect('view_admin')
    return render(request, 'register_admin.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'permissions': User_Permissions, 'error': err})

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

@check_authentication
def view_admin(request):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    univ = TblUniversity.objects.all()
    All_Admin = TblPermissions.objects.all()
    # PERMISSION TO VIEW
    if not User_Permissions.can_view:
        return redirect('dashboard')
    return render(request, 'view_admin.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'permissions': User_Permissions, 'error': err,
                   'all_admin': All_Admin})


@check_authentication
def update_admin(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    Update_Admin = TblAdmin.objects.get(id=id)
    Update_Permissions = TblPermissions.objects.get(admin_id=Update_Admin)
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
    return render(request, 'update_admin.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'permissions': User_Permissions,
                   'update_admin': Update_Admin, 'update_permissions': Update_Permissions, 'error': err})

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

@check_authentication
def delete_admin(request, id):
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    # CAN'T DELETE OWN PROFILE
    if user.id == id:
        return redirect('view_admin')

    # PERMISSION TO DELETE
    if not User_Permissions.can_delete:
        return redirect('view_admin')
    else:
        Del_Admin = Account.objects.get(id=id)
        Del_Admin.delete()
        return redirect('view_admin')


@check_authentication
def logout_page(request):
    print(request.user)
    logout(request)
    return redirect('login')


# ----------------------------For-Student----------------------------------


@check_authentication
def view_requests(request):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    univ = TblUniversity.objects.all()
    New_Request = TblUsers.objects.filter(is_approved=False)
    # PERMISSION TO VIEW
    if not User_Permissions.can_view:
        return redirect('dashboard')
    return render(request, 'view_student_new_request.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'permissions': User_Permissions, 'error': err,
                   'new_request': New_Request})


@check_authentication
def approve_student(request, id):
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    Student = TblUsers.objects.get(id=id)
    # PERMISSION TO UPDATE
    if not User_Permissions.can_edit:
        return redirect('dashboard')
    Student.is_approved = True
    Student.save()
    return redirect('view_requests')


@check_authentication
def decline_student(request, id):
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    # PERMISSION TO DELETE
    if not User_Permissions.can_delete:
        return redirect('view_requests')
    else:
        Del_Student = Account.objects.get(id=id)
        Del_Student.delete()
        return redirect('view_requests')


@check_authentication
def view_accepted_students(request):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    univ = TblUniversity.objects.all()
    Accepted_Students = TblUsers.objects.filter(is_approved=True)
    # PERMISSION TO VIEW
    if not User_Permissions.can_view:
        return redirect('dashboard')
    return render(request, 'view_accepted_students.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'permissions': User_Permissions, 'error': err,
                   'accepted_students': Accepted_Students})


@check_authentication
def print_permissions(request):
    print(request.user)
    print([request.user.has_perm(p.content_type.app_label + '.' + p.codename) for p in Permission.objects.filter(content_type__app_label='User',
                                                                                      content_type__model='account')])
    print(request.user.user_permissions.all())
    print([p.content_type.app_label for p in request.user.user_permissions.all()])
    print([request.user.has_perm(('User' if p.content_type.model == 'account' else p.content_type.model) + '.' + p.codename) for p in request.user.user_permissions.all()])
    return HttpResponse('Hello')
