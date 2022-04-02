from django.shortcuts import redirect, render

from University.models import TblCourses, TblDepartments, TblInstitutes, TblUniversity

from .serializers import RegistrationSerializer, TblAdminSerializer

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Permission

from User.models import Account, TblAdmin, TblUsers

from django.contrib.auth.decorators import login_required

from utils.permissions import give_admin_permission, give_director_permission, give_principal_permission, \
    give_hod_permission, give_faculty_permission, give_permission_for_model, remove_permission
from django.contrib.auth.models import Group

from guardian.shortcuts import assign_perm, get_objects_for_user, get_users_with_perms


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


@login_required
def profile(request):
    err = str()
    User_Admin = TblAdmin.objects.get(account_id=request.user)
    univ = TblUniversity.objects.all()
    if request.POST:
        nm = request.POST['nm1']
        cno = request.POST['cno1']
        prof1 = request.FILES.get('prof1')
        User_Admin.admin_name = nm
        User_Admin.admin_contact_number = cno
        if prof1 is not None:
            User_Admin.admin_image = prof1
        User_Admin.save()
    return render(request, 'profile.html',
                  {'Users': request.user,
                   'admin': User_Admin,
                   'univ': univ,
                   'error': err})


@login_required
def change_password(request):
    err = suc = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
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
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                   'success': suc})


@login_required
def register_admin(request):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    if not user.has_perm('User.add_account'):
        err = "You are not authorized to register a new admin."
        univ = TblUniversity.objects.all()
        superuser_list = Account.objects.filter(is_staff=True)
        admin_list = TblAdmin.objects.filter(account_id__in=superuser_list)
        return render(request, 'view_admin.html',
                      {'Users': user,
                       'admin': User_Admin,
                       'univ': univ,
                       'error': err,
                       'admin_list': admin_list
                       })
    if request.POST:
        em = request.POST['em1']
        pwd = request.POST['pass1']
        nm = request.POST['nm1']
        cno = request.POST['cno1']
        prof1 = request.FILES.get('prof1')
        can_add = request.POST.get('can_add')
        can_update = request.POST.get('can_update')
        can_delete = request.POST.get('can_delete')
        serializer = RegistrationSerializer(
            data={'email': em, 'is_admin': True, 'is_active': True, 'is_staff': True},
            partial=True)
        if serializer.is_valid():
            try:
                account = serializer.save()
            except Exception:
                if account:
                    account.delete()
                err = 'error creating superuser'
                return render(request, 'register_admin.html', {'Users': user, 'admin': User_Admin, 'error': err})
            account.set_password(pwd)
            account.save()
            admin_serializer = TblAdminSerializer(
                data={'account_id': account.id, 'admin_name': nm, 'admin_contact_number': cno, 'admin_image': prof1},
                partial=True)
            if admin_serializer.is_valid():
                try:
                    admin = admin_serializer.save()
                except Exception:
                    if admin:
                        admin.delete()
                    account.delete()
                    err = 'error creating user admin'
                    return render(request, 'register_admin.html', {'Users': user, 'admin': User_Admin, 'error': err})
                try:
                    give_permission_for_model(account, 'view_account', Account)
                    if can_add is not None:
                        give_permission_for_model(account, 'add_account', Account)
                    if can_update is not None:
                        give_permission_for_model(account, 'change_account', Account)
                    if can_delete is not None:
                        give_permission_for_model(account, 'delete_account', Account)
                    give_admin_permission(account)
                except (Permission.DoesNotExist, Group.DoesNotExist):
                    err = """
                    Technical Error Occurred: 
                    unable to provide permissions to the user"""
                    admin.delete()
                    account.delete()
                    return render(request, 'register_admin.html', {'Users': user, 'admin': User_Admin, 'error': err})
                return redirect('view_admin')
            else:
                err = "Invalid Input"
                return render(request, 'register_admin.html', {'Users': user, 'admin': User_Admin, 'error': err})
        else:
            err = serializer.errors['email'][0]
            print(type(serializer.errors['email'][0]), serializer.errors['email'][0])
            return render(request, 'register_admin.html', {'Users': user, 'admin': User_Admin, 'error': err})
    return render(request, 'register_admin.html', {'Users': user, 'admin': User_Admin, 'error': err})


@login_required
def register_director(request):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    if not user.has_perm('User.add_account'):
        err = "You are not authorized to register a new director."
        univ = TblUniversity.objects.all()
        director_list = Account.objects.filter(groups__name='director')
        director_list_admin = TblAdmin.objects.filter(account_id__in=director_list)
        return render(request, 'view_director.html',
                      {
                          'Users': user,
                          'admin': User_Admin,
                          'univ': univ,
                          'error': err,
                          'director_list_admin': director_list_admin,
                      })
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        contact_number = request.POST['contactNumber']
        profile_picture = request.FILES.get('profilePicture')
        university_id = request.POST['university']
        serializer = RegistrationSerializer(
            data={'email': email, 'is_admin': True, 'is_active': True}, partial=True)
        if serializer.is_valid():
            try:
                account = serializer.save()
            except Exception:
                if account:
                    account.delete()
                err = "error creating director"
                return render(request, 'register_admin.html',
                              {'Users': user, 'admin': User_Admin, 'error': err, 'univ': univ})
            account.set_password(password)
            account.save()
            admin_serializer = TblAdminSerializer(
                data={'account_id': account.id, 'admin_name': name, 'admin_contact_number': contact_number,
                      'admin_image': profile_picture},
                partial=True)
            if admin_serializer.is_valid():
                try:
                    admin = admin_serializer.save()
                except Exception:
                    if admin:
                        admin.delete()
                    account.delete()
                    err = 'error creating director admin'
                    return render(request, 'register_director.html',
                                  {'Users': user, 'admin': User_Admin, 'error': err, 'univ': univ})
                try:
                    give_director_permission(account)
                    assigned_university = TblUniversity.objects.get(id=university_id)
                    assign_perm('view_tbluniversity', account, assigned_university)
                except (Permission.DoesNotExist, Group.DoesNotExist):
                    err = "Technical Error Occurred:"
                    admin.delete()
                    account.delete()
                    return render(request, 'register_director.html',
                                  {'Users': user, 'admin': User_Admin, 'error': err, 'univ': univ})
                return redirect('view_director')
            else:
                err = admin_serializer.errors
                return render(request, 'register_director.html',
                              {'Users': user, 'admin': User_Admin, 'error': err, 'univ': univ})
        else:
            err = serializer.errors
            univ = TblUniversity.objects.all()
            director_list = Account.objects.filter(groups__name='director')
            director_list_admin = TblAdmin.objects.filter(account_id__in=director_list)
            return render(request, 'view_director.html',
                          {
                              'Users': user,
                              'admin': User_Admin,
                              'univ': univ,
                              'error': err,
                              'director_list_admin': director_list_admin,
                          })
    return render(request, 'register_director.html', {'Users': user, 'admin': User_Admin, 'error': err, 'univ': univ})


@login_required
def register_principal(request):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    if user.is_staff:
        univ = TblUniversity.objects.all()
    elif user.groups.get(name='director'):
        univ = get_objects_for_user(request.user, 'University.view_tbluniversity').filter()
    if not user.has_perm('User.add_account'):
        err = "You are not authorized to register a new principal."
        principal_list = Account.objects.filter(groups__name='principal')
        principal_list_admin = TblAdmin.objects.filter(account_id__in=principal_list)
        return render(request, 'view_principal.html',
                      {
                          'Users': user,
                          'admin': User_Admin,
                          'univ': univ,
                          'error': err,
                          'principal_list_admin': principal_list_admin,
                      })
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        contact_number = request.POST['contactNumber']
        profile_picture = request.FILES.get('profilePicture')
        selected_university_id = request.POST['university']
        selected_institute_id = request.POST['institutes']
        serializer = RegistrationSerializer(
            data={'email': email, 'is_admin': True, 'is_active': True}, partial=True)
        if serializer.is_valid():
            try:
                account = serializer.save()
            except Exception:
                if account:
                    account.delete()
                err = "error creating principal"
                return render(request, 'register_principal.html', {'Users': user, 'admin': User_Admin, 'error': err, 'univ': univ})
            account.set_password(password)
            account.save()
            admin_serializer = TblAdminSerializer(
                data={'account_id': account.id, 'admin_name': name, 'admin_contact_number': contact_number,
                      'admin_image': profile_picture},
                partial=True)
            if admin_serializer.is_valid():
                try:
                    admin = admin_serializer.save()
                except Exception:
                    if admin:
                        admin.delete()
                    account.delete()
                    err = 'error creating principal admin'
                    return render(request, 'register_principal.html',
                                  {'Users': user, 'admin': User_Admin, 'error': err, 'univ': univ})
                try:
                    give_principal_permission(account)
                    selected_university = TblUniversity.objects.get(id=selected_university_id)
                    selected_institute = TblInstitutes.objects.get(id=selected_institute_id)
                    if request.user.groups.filter(name='director').exists():
                        director = request.user
                    else:
                        director = get_users_with_perms(selected_university).filter(groups__name='director')[0]
                    assign_perm('view_account', director, account)
                    assign_perm('change_account', director, account)
                    assign_perm('delete_account', director, account)
                    assign_perm('view_tbluniversity', account, selected_university)
                    assign_perm('view_tblinstitutes', account, selected_institute)
                except (Permission.DoesNotExist, Group.DoesNotExist):
                    err = "Technical Error Occurred"
                    admin.delete()
                    account.delete()
                    return render(request, 'register_principal.html',
                                  {'Users': user, 'admin': User_Admin, 'error': err, 'univ': univ})
                return redirect('view_principal')
            else:
                err = admin_serializer.errors
                return render(request, 'register_principal.html', {'Users': user, 'admin': User_Admin, 'error': err, 'univ': univ})
        else:
            err = serializer.errors
            univ = TblUniversity.objects.all()
            principal_list = Account.objects.filter(groups__name='principal')
            principal_list_admin = TblAdmin.objects.filter(account_id__in=principal_list)
            return render(request, 'view_principal.html',
                          {
                              'Users': user,
                              'admin': User_Admin,
                              'univ': univ,
                              'error': err,
                              'principal_list_admin': principal_list_admin,
                          })
    return render(request, 'register_principal.html', {'Users': user, 'admin': User_Admin, 'error': err, 'univ': univ})


@login_required
def register_hod(request):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    if user.is_staff:
        univ = TblUniversity.objects.all()
        # ins = None
    elif user.groups.filter(name='director').exists():
        univ = get_objects_for_user(request.user, 'University.view_tbluniversity').filter()
        # ins = get_objects_for_user(request.user, 'University.view_tblinstitutes').filter()
    elif user.groups.filter(name='principal').exists():
        univ = get_objects_for_user(request.user, 'University.view_tbluniversity').filter()
        # ins = get_objects_for_user(request.user, 'University.view_tblinstitutes').filter()
    if not user.has_perm('User.add_account'):
        err = "You are not authorized to register a new HOD."
        hod_list = Account.objects.filter(groups__name='hod')
        hod_list_admin = TblAdmin.objects.filter(account_id__in=hod_list)
        return render(request, 'view_hod.html',
                      {
                          'Users': user,
                          'admin': User_Admin,
                          'univ': univ,
                          'error': err,
                          'hod_list_admin': hod_list_admin,
                      })
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        contact_number = request.POST['contactNumber']
        profile_picture = request.FILES.get('profilePicture')
        selected_department_id = request.POST['department']
        serializer = RegistrationSerializer(
            data={'email': email, 'is_admin': True, 'is_active': True}, partial=True)
        if serializer.is_valid():
            try:
                account = serializer.save()
            except Exception:
                if account:
                    account.delete()
                err = "error creating HOD"
                return render(request, 'register_hod.html', {'Users': user, 'admin': User_Admin, 'error': err, 'univ': univ})
            account.set_password(password)
            account.save()
            admin_serializer = TblAdminSerializer(
                data={'account_id': account.id, 'admin_name': name, 'admin_contact_number': contact_number,
                      'admin_image': profile_picture},
                partial=True)
            if admin_serializer.is_valid():
                try:
                    admin = admin_serializer.save()
                except Exception:
                    if admin:
                        admin.delete()
                    account.delete()
                    err = 'error creating HOD admin'
                    return render(request, 'register_hod.html', {'Users': user, 'admin': User_Admin, 'error': err, 'univ': univ})
                try:
                    give_hod_permission(account)
                    selected_department = TblDepartments.objects.get(id=selected_department_id)
                    assign_perm('view_tbldepartments', account, selected_department)
                    if request.user.groups.filter(name='principal').exists():
                        principal = request.user
                    else:
                        principal = get_users_with_perms(selected_department.institute_id).filter(groups__name='principal')[0]
                    assign_perm('view_account', principal, account)
                    assign_perm('change_account', principal, account)
                    assign_perm('delete_account', principal, account)
                    director = get_users_with_perms(selected_department.institute_id.university_id).filter(groups__name='director')[0]
                    assign_perm('view_account', director, account)
                    assign_perm('change_account', director, account)
                    assign_perm('delete_account', director, account)
                    assign_perm('view_tbluniversity', account, selected_department.institute_id.university_id)
                    assign_perm('view_tblinstitutes', account, selected_department.institute_id)
                    assign_perm('view_tbldepartments', account, selected_department)
                except (Permission.DoesNotExist, Group.DoesNotExist):
                    err = "Technical Error Occurred"
                    admin.delete()
                    account.delete()
                    return render(request, 'register_hod.html', {'Users': user, 'admin': User_Admin, 'error': err, 'univ': univ})
                return redirect('view_hod')
            else:
                err = admin_serializer.errors
                return render(request, 'register_hod.html', {'Users': user, 'admin': User_Admin, 'error': err, 'univ': univ})
        else:
            err = serializer.errors
            univ = TblUniversity.objects.all()
            hod_list = Account.objects.filter(groups__name='hod')
            hod_list_admin = TblAdmin.objects.filter(account_id__in=hod_list)
            return render(request, 'view_hod.html',
                          {
                              'Users': user,
                              'admin': User_Admin,
                              'univ': univ,
                              'error': err,
                              'hod_list_admin': hod_list_admin,
                          })
    return render(request, 'register_hod.html', {'Users': user, 'admin': User_Admin, 'error': err, 'univ': univ})


@login_required
def register_faculty(request):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    if user.is_staff:
        univ = TblUniversity.objects.all()
        # ins = None
    elif user.groups.filter(name='director').exists():
        univ = get_objects_for_user(request.user, 'University.view_tbluniversity').filter()
        # ins = get_objects_for_user(request.user, 'University.view_tblinstitutes').filter()
    elif user.groups.filter(name='principal').exists():
        univ = get_objects_for_user(request.user, 'University.view_tbluniversity').filter()
        # ins = get_objects_for_user(request.user, 'University.view_tblinstitutes').filter()
    elif user.groups.filter(name='hod').exists():
        univ = get_objects_for_user(request.user, 'University.view_tbluniversity').filter()
        # ins = get_objects_for_user(request.user, 'University.view_tblinstitutes').filter()
    if not user.has_perm('User.add_account'):
        err = "You are not authorized to register a new faculty."
        faculty_list = Account.objects.filter(groups__name='faculty')
        faculty_list_admin = TblAdmin.objects.filter(account_id__in=faculty_list)
        return render(request, 'view_faculty.html',
                      {
                          'Users': user,
                          'admin': User_Admin,
                          'univ': univ,
                          'error': err,
                          'faculty_list_admin': faculty_list_admin,
                      })
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        contact_number = request.POST['contactNumber']
        profile_picture = request.FILES.get('profilePicture')
        selected_course_id = request.POST['courses']
        serializer = RegistrationSerializer(
            data={'email': email, 'is_admin': True, 'is_active': True}, partial=True)
        if serializer.is_valid():
            try:
                account = serializer.save()
            except Exception:
                if account:
                    account.delete()
                err = "error creating director"
                return render(request, 'register_faculty.html', {'Users': user, 'admin': User_Admin, 'error': err, 'univ': univ})
            account.set_password(password)
            account.save()
            admin_serializer = TblAdminSerializer(
                data={'account_id': account.id, 'admin_name': name, 'admin_contact_number': contact_number,
                      'admin_image': profile_picture},
                partial=True)
            if admin_serializer.is_valid():
                try:
                    admin = admin_serializer.save()
                except Exception:
                    if admin:
                        admin.delete()
                    account.delete()
                    err = 'error creating director admin'
                    return render(request, 'register_faculty.html', {'Users': user, 'admin': User_Admin, 'error': err, 'univ': univ})
                try:
                    give_faculty_permission(account)
                    selected_course = TblCourses.objects.get(id=selected_course_id)
                    assign_perm('view_tblcourses', account, selected_course)
                    if request.user.groups.filter(name='hod').exists():
                        hod = request.user
                    else:
                        hod = get_users_with_perms(selected_course.department_id).filter(groups__name='hod')[0]
                    assign_perm('view_account', hod, account)
                    assign_perm('change_account', hod, account)
                    assign_perm('delete_account', hod, account)
                    principal = get_users_with_perms(selected_course.department_id.institute_id).filter(groups__name='principal')[0]
                    assign_perm('view_account', principal, account)
                    assign_perm('change_account', principal, account)
                    assign_perm('delete_account', principal, account)
                    director = get_users_with_perms(selected_course.department_id.institute_id.university_id).filter(groups__name='director')[0]
                    assign_perm('view_account', director, account)
                    assign_perm('change_account', director, account)
                    assign_perm('delete_account', director, account)
                    assign_perm('view_tbluniversity', account, selected_course.department_id.institute_id.university_id)
                    assign_perm('view_tblinstitutes', account, selected_course.department_id.institute_id)
                    assign_perm('view_tbldepartments', account, selected_course.department_id)
                    assign_perm('view_tblcourses', account, selected_course)
                except (Permission.DoesNotExist, Group.DoesNotExist):
                    err = "Technical Error Occurred"
                    admin.delete()
                    account.delete()
                    return render(request, 'register_faculty.html', {'Users': user, 'admin': User_Admin, 'error': err, 'univ': univ})
                return redirect('view_faculty')
            else:
                err = admin_serializer.errors
                return render(request, 'register_faculty.html', {'Users': user, 'admin': User_Admin, 'error': err, 'univ': univ})
        else:
            err = serializer.errors
            univ = TblUniversity.objects.all()
            faculty_list = Account.objects.filter(groups__name='faculty')
            faculty_list_admin = TblAdmin.objects.filter(account_id__in=faculty_list)
            return render(request, 'view_faculty.html',
                          {
                              'Users': user,
                              'admin': User_Admin,
                              'univ': univ,
                              'error': err,
                              'faculty_list_admin': faculty_list_admin,
                          })
    return render(request, 'register_faculty.html', {'Users': user, 'admin': User_Admin, 'error': err, 'univ': univ})


def sel_institute(request):
    university_id = request.GET.get('univ_id')
    institutes = TblInstitutes.objects.filter(university_id=university_id)
    return render(request, 'select_option.html', {'institutes': institutes})


def sel_department(request):
    institute_id = request.GET.get('institute_id')
    departments = TblDepartments.objects.filter(institute_id=institute_id)
    return render(request, 'select_option.html', {'departments': departments})


def sel_courses(request):
    department_id = request.GET.get('department_id')
    courses = TblCourses.objects.filter(department_id=department_id)
    return render(request, 'select_option.html', {'courses': courses})


@login_required
def view_admin(request):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    superuser_list = Account.objects.filter(is_staff=True)
    admin_list = TblAdmin.objects.filter(account_id__in=superuser_list)
    univ = TblUniversity.objects.all()
    return render(request, 'view_admin.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ,
                   'error': err,
                   'admin_list': admin_list})


@login_required
def view_director(request):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    director_list = Account.objects.filter(groups__name='director')
    director_list_admin = TblAdmin.objects.filter(account_id__in=director_list)
    return render(request, 'view_director.html',
                  {
                      'Users': user,
                      'admin': User_Admin,
                      'univ': univ,
                      'error': err,
                      'director_list_admin': director_list_admin,
                  })


@login_required
def view_principal(request):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    principal_list = Account.objects.filter(groups__name='principal')
    principal_list_admin = TblAdmin.objects.filter(account_id__in=principal_list)
    return render(request, 'view_principal.html',
                  {
                      'Users': user,
                      'admin': User_Admin,
                      'univ': univ,
                      'error': err,
                      'principal_list_admin': principal_list_admin,
                  })


@login_required
def view_hod(request):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    hod_list = Account.objects.filter(groups__name='hod')
    hod_list_admin = TblAdmin.objects.filter(account_id__in=hod_list)
    return render(request, 'view_hod.html',
                  {
                      'Users': user,
                      'admin': User_Admin,
                      'univ': univ,
                      'error': err,
                      'hod_list_admin': hod_list_admin,
                  })


@login_required
def view_faculty(request):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    faculty_list = Account.objects.filter(groups__name='faculty')
    faculty_list_admin = TblAdmin.objects.filter(account_id__in=faculty_list)
    return render(request, 'view_faculty.html',
                  {
                      'Users': user,
                      'admin': User_Admin,
                      'univ': univ,
                      'error': err,
                      'faculty_list_admin': faculty_list_admin,
                  })


@login_required
def update_admin(request, key):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    Update_Admin = TblAdmin.objects.get(id=key)
    admin_list = TblAdmin.objects.filter(account_id__in=Account.objects.filter(is_staff=True))
    # RESTRICTED TO UPDATE OWN PROFILE
    # if User_Admin.id == id:
    #     return redirect('view_admin')
    # PERMISSION TO UPDATE
    if not user.has_perm('User.change_account'):
        err = "You are not authorized to update any admin."
        return render(request, 'view_admin.html',
                      {'Users': user,
                       'admin': User_Admin,
                       'univ': univ,
                       'error': err,
                       'admin_list': admin_list})
    if request.POST:
        name = request.POST['nm1']
        contact_no = request.POST['cno1']
        profile_photo = request.FILES.get('prof1')
        can_add = request.POST.get('can_add')
        can_change = request.POST.get('can_change')
        can_delete = request.POST.get('can_delete')
        if not Update_Admin.admin_name == name:
            Update_Admin.admin_name = name
        if not Update_Admin.admin_contact_number == contact_no:
            Update_Admin.admin_contact_number = contact_no
        if profile_photo is not None:
            Update_Admin.admin_image = profile_photo
        if can_add is not None:
            give_permission_for_model(Update_Admin.account_id, 'add_account', Account)
        else:
            remove_permission(Update_Admin.account_id, 'add_account', Account)
        if can_change is not None:
            give_permission_for_model(Update_Admin.account_id, 'change_account', Account)
        else:
            remove_permission(Update_Admin.account_id, 'change_account', Account)
        if can_delete is not None:
            give_permission_for_model(Update_Admin.account_id, 'delete_account', Account)
        else:
            remove_permission(Update_Admin.account_id, 'delete_account', Account)
        Update_Admin.save()
        return render(request, 'view_admin.html',
                      {'Users': user,
                       'admin': User_Admin,
                       'univ': univ,
                       'error': err,
                       'admin_list': admin_list})
    return render(request, 'update_admin.html',
                  {'Users': user,
                   'admin': User_Admin,
                   'univ': univ,
                   'update_admin': Update_Admin,
                   'can_view': 1 if Update_Admin.account_id.has_perm('User.view_account') else 0,
                   'can_add': 1 if Update_Admin.account_id.has_perm('User.add_account') else 0,
                   'can_change': 1 if Update_Admin.account_id.has_perm('User.change_account') else 0,
                   'can_delete': 1 if Update_Admin.account_id.has_perm('User.delete_account') else 0,
                   'error': err})


@login_required
def update_director(request, key):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    updateDirector = TblAdmin.objects.get(id=key)
    director_list = Account.objects.filter(groups__name='director')
    director_list_admin = TblAdmin.objects.filter(account_id__in=director_list)
    university = None
    if get_objects_for_user(updateDirector.account_id, 'University.view_tbluniversity').exists():
        university = get_objects_for_user(updateDirector.account_id, 'University.view_tbluniversity')[0]
    if not user.is_staff or not user.has_perm('User.change_account'):
        err = "You are not authorized to update any director."
        return render(request, 'view_director.html',
                      {'Users': user,
                       'admin': User_Admin,
                       'univ': univ,
                       'error': err,
                       'director_list_admin': director_list_admin})
    if request.POST:
        name = request.POST['nm1']
        contact_no = request.POST['cno1']
        profile_photo = request.FILES.get('prof1')
        if not updateDirector.admin_name == name:
            updateDirector.admin_name = name
        if not updateDirector.admin_contact_number == contact_no:
            updateDirector.admin_contact_number = contact_no
        if profile_photo is not None:
            updateDirector.admin_image = profile_photo
        updateDirector.save()
        return render(request, 'view_director.html',
                      {'Users': user,
                       'admin': User_Admin,
                       'univ': univ,
                       'error': err,
                       'director_list_admin': director_list_admin})
    return render(request, 'update_director.html',
                  {'Users': user,
                   'admin': User_Admin,
                   'univ': univ,
                   'update_director': updateDirector,
                   'university': university,
                   'error': err})


@login_required
def update_principal(request, key):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    updatePrincipal = TblAdmin.objects.get(id=key)
    principal_list = Account.objects.filter(groups__name='principal')
    principal_list_admin = TblAdmin.objects.filter(account_id__in=principal_list)
    university = None
    institute = None
    if get_objects_for_user(updatePrincipal.account_id, 'University.view_tbluniversity').exists():
        university = get_objects_for_user(updatePrincipal.account_id, 'University.view_tbluniversity')[0]
    if get_objects_for_user(updatePrincipal.account_id, 'University.view_tblinstitutes').exists():
        institute = get_objects_for_user(updatePrincipal.account_id, 'University.view_tblinstitutes')[0]
    if not user.is_staff or not user.has_perm('User.change_account'):
        err = "You are not authorized to update any principal."
        return render(request, 'view_principal.html',
                      {'Users': user,
                       'admin': User_Admin,
                       'univ': univ,
                       'error': err,
                       'principal_list_admin': principal_list_admin})
    if request.POST:
        name = request.POST['nm1']
        contact_no = request.POST['cno1']
        profile_photo = request.FILES.get('prof1')
        if not updatePrincipal.admin_name == name:
            updatePrincipal.admin_name = name
        if not updatePrincipal.admin_contact_number == contact_no:
            updatePrincipal.admin_contact_number = contact_no
        if profile_photo is not None:
            updatePrincipal.admin_image = profile_photo
        updatePrincipal.save()
        return render(request, 'view_principal.html',
                      {'Users': user,
                       'admin': User_Admin,
                       'univ': univ,
                       'error': err,
                       'principal_list_admin': principal_list_admin})
    return render(request, 'update_principal.html',
                  {'Users': user,
                   'admin': User_Admin,
                   'univ': univ,
                   'update_principal': updatePrincipal,
                   'university': university,
                   'institute': institute,
                   'error': err})


@login_required
def update_hod(request, key):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    updateHod = TblAdmin.objects.get(id=key)
    hod_list = Account.objects.filter(groups__name='hod')
    hod_list_admin = TblAdmin.objects.filter(account_id__in=hod_list)
    university = None
    institute = None
    department = None
    if get_objects_for_user(updateHod.account_id, 'University.view_tbluniversity').exists():
        university = get_objects_for_user(updateHod.account_id, 'University.view_tbluniversity')[0]
    if get_objects_for_user(updateHod.account_id, 'University.view_tblinstitutes').exists():
        institute = get_objects_for_user(updateHod.account_id, 'University.view_tblinstitutes')[0]
    if get_objects_for_user(updateHod.account_id, 'University.view_tbldepartments').exists():
        department = get_objects_for_user(updateHod.account_id, 'University.view_tbldepartments')[0]
    if not user.is_staff or not user.has_perm('User.change_account'):
        err = "You are not authorized to update any hod."
        return render(request, 'view_hod.html',
                      {'Users': user,
                       'admin': User_Admin,
                       'univ': univ,
                       'error': err,
                       'hod_list_admin': hod_list_admin})
    if request.POST:
        name = request.POST['nm1']
        contact_no = request.POST['cno1']
        profile_photo = request.FILES.get('prof1')
        if not updateHod.admin_name == name:
            updateHod.admin_name = name
        if not updateHod.admin_contact_number == contact_no:
            updateHod.admin_contact_number = contact_no
        if profile_photo is not None:
            updateHod.admin_image = profile_photo
        updateHod.save()
        return render(request, 'view_hod.html',
                      {'Users': user,
                       'admin': User_Admin,
                       'univ': univ,
                       'error': err,
                       'hod_list_admin': hod_list_admin})
    return render(request, 'update_hod.html',
                  {'Users': user,
                   'admin': User_Admin,
                   'univ': univ,
                   'update_hod': updateHod,
                   'university': university,
                   'institute': institute,
                   'department': department,
                   'error': err})


@login_required
def update_faculty(request, key):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    updateFaculty = TblAdmin.objects.get(id=key)
    faculty_list = Account.objects.filter(groups__name='faculty')
    faculty_list_admin = TblAdmin.objects.filter(account_id__in=faculty_list)
    university = None
    institute = None
    department = None
    course = None
    if get_objects_for_user(updateFaculty.account_id, 'University.view_tbluniversity').exists():
        university = get_objects_for_user(updateFaculty.account_id, 'University.view_tbluniversity')[0]
    if get_objects_for_user(updateFaculty.account_id, 'University.view_tblinstitutes').exists():
        institute = get_objects_for_user(updateFaculty.account_id, 'University.view_tblinstitutes')[0]
    if get_objects_for_user(updateFaculty.account_id, 'University.view_tbldepartments').exists():
        department = get_objects_for_user(updateFaculty.account_id, 'University.view_tbldepartments')[0]
    if get_objects_for_user(updateFaculty.account_id, 'University.view_tblcourses').exists():
        course = get_objects_for_user(updateFaculty.account_id, 'University.view_tblcourses')[0]
    if not user.is_staff or not user.has_perm('User.change_account'):
        err = "You are not authorized to update any faculty."
        return render(request, 'view_faculty.html',
                      {'Users': user,
                       'admin': User_Admin,
                       'univ': univ,
                       'error': err,
                       'faculty_list_admin': faculty_list_admin})
    if request.POST:
        name = request.POST['nm1']
        contact_no = request.POST['cno1']
        profile_photo = request.FILES.get('prof1')
        if not updateFaculty.admin_name == name:
            updateFaculty.admin_name = name
        if not updateFaculty.admin_contact_number == contact_no:
            updateFaculty.admin_contact_number = contact_no
        if profile_photo is not None:
            updateFaculty.admin_image = profile_photo
        updateFaculty.save()
        return render(request, 'view_faculty.html',
                      {'Users': user,
                       'admin': User_Admin,
                       'univ': univ,
                       'error': err,
                       'faculty_list_admin': faculty_list_admin})
    return render(request, 'update_faculty.html',
                  {'Users': user,
                   'admin': User_Admin,
                   'univ': univ,
                   'update_faculty': updateFaculty,
                   'university': university,
                   'institute': institute,
                   'department': department,
                   'course': course,
                   'error': err})


def update_institute(request):
    university_id = request.GET.getlist('univ_id[]')
    institutes = TblInstitutes.objects.filter(university_id__in=university_id)
    return render(request, 'update_option.html', {'institutes': institutes})


def update_department(request):
    institute_id = request.GET.getlist('institute_id[]')
    departments = TblDepartments.objects.filter(institute_id__in=institute_id)
    return render(request, 'update_option.html', {'departments': departments})


def update_courses(request):
    department_id = request.GET.getlist('department_id[]')
    courses = TblCourses.objects.filter(department_id__in=department_id)
    return render(request, 'update_option.html', {'courses': courses})


@login_required
def delete_admin(request, key):
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    # CAN'T DELETE OWN PROFILE
    if user.id == key:
        return redirect('view_admin')

    # PERMISSION TO DELETE
    if not user.has_perm('User.delete_account'):
        admin_list = TblAdmin.objects.filter(account_id__in=Account.objects.filter(is_staff=True))
        err = "You are not authorized to delete any admin."
        return render(request, 'view_admin.html',
                      {'Users': user,
                       'admin': User_Admin,
                       'univ': univ,
                       'error': err,
                       'admin_list': admin_list})
    else:
        Del_Admin = Account.objects.get(id=key)
        Del_Admin.delete()
        return redirect('view_admin')


@login_required
def delete_director(request, key):
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    # CAN'T DELETE OWN PROFILE
    if user.id == key:
        return redirect('view_director')

    # PERMISSION TO DELETE
    if not user.has_perm('User.delete_account'):
        director_list_admin = TblAdmin.objects.filter(account_id__in=Account.objects.filter(groups__name='director'))
        err = "You are not authorized to delete any director."
        return render(request, 'view_director.html',
                      {'Users': user,
                       'admin': User_Admin,
                       'univ': univ,
                       'error': err,
                       'admin_list': director_list_admin})
    else:
        Del_Admin = Account.objects.get(id=key)
        Del_Admin.delete()
        return redirect('view_director')


@login_required
def delete_principal(request, key):
    pass


@login_required
def delete_hod(request, key):
    pass


@login_required
def delete_faculty(request, key):
    pass


@login_required
def logout_page(request):
    print(request.user)
    logout(request)
    return redirect('login')


# ----------------------------For-Student----------------------------------


@login_required
def view_requests(request):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    new_request = None
    if user.is_staff:
        new_request = TblUsers.objects.filter(is_approved=False)
    elif user.groups.filter(name='director').exists():
        if get_objects_for_user(user, 'University.view_tbluniversity').exists():
            new_request = TblUsers.objects.filter(is_approved=False) & TblUsers.objects.filter(
                institute_id__in=get_objects_for_user(user, 'University.view_tblinstitutes'))
    elif user.groups.filter(name='principal').exists():
        if get_objects_for_user(user, 'University.view_tblinstitutes').exists():
            new_request = TblUsers.objects.filter(is_approved=False) & TblUsers.objects.filter(
                institute_id__in=get_objects_for_user(user, 'University.view_tblinstitutes'))
    elif user.groups.filter(name='hod').exists():
        if get_objects_for_user(user, 'University.view_tbldepartments').exists():
            new_request = TblUsers.objects.filter(is_approved=False) & TblUsers.objects.filter(
                department_id__in=get_objects_for_user(user, 'University.view_tbldepartments'))
    if not user.has_perm('User.change_account'):
        return redirect('dashboard')
    return render(request, 'view_student_new_request.html',
                  {'Users': user,
                   'admin': User_Admin,
                   'univ': univ,
                   'error': err,
                   'new_request': new_request})


@login_required
def approve_student(request, id):
    user = request.user
    Student = TblUsers.objects.get(id=id)
    # PERMISSION TO UPDATE
    if not user.has_perm('User.change_account') or not TblUsers.objects.filter(account_id=user).exists():
        return redirect('dashboard')
    Student.is_approved = True
    Student.save()
    return redirect('view_requests')


@login_required
def decline_student(request, id):
    user = request.user
    # PERMISSION TO DELETE
    if not user.has_perm('User.delete_account'):
        return redirect('view_requests')
    else:
        Del_Student = Account.objects.get(id=id)
        Del_Student.delete()
        return redirect('view_requests')


@login_required
def view_accepted_students(request):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    accepted_students = None
    if user.is_staff:
        accepted_students = TblUsers.objects.filter(is_approved=True)
    elif user.groups.filter(name='director').exists():
        if get_objects_for_user(user, 'University.view_tbluniversity').exists():
            accepted_students = TblUsers.objects.filter(is_approved=True) & TblUsers.objects.filter(
                institute_id__in=get_objects_for_user(user, 'University.view_tblinstitutes'))
    elif user.groups.filter(name='principal').exists():
        if get_objects_for_user(user, 'University.view_tblinstitutes').exists():
            accepted_students = TblUsers.objects.filter(is_approved=True) & TblUsers.objects.filter(
                institute_id__in=get_objects_for_user(user, 'University.view_tblinstitutes'))
    elif user.groups.filter(name='hod').exists():
        if get_objects_for_user(user, 'University.view_tbldepartments').exists():
            accepted_students = TblUsers.objects.filter(is_approved=True) & TblUsers.objects.filter(
                department_id__in=get_objects_for_user(user, 'University.view_tbldepartments'))
    # PERMISSION TO VIEW
    if not user.has_perm('User.view_account'):
        return redirect('dashboard')
    return render(request, 'view_accepted_students.html',
                  {'Users': user,
                   'admin': User_Admin,
                   'univ': univ,
                   'error': err,
                   'accepted_students': accepted_students})
