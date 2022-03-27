from django.shortcuts import render, redirect
from django.contrib import messages

from User.models import TblAdmin

from University.models import TblUniversity, TblInstitutes, TblDepartments, TblCourses

from django.contrib.auth.decorators import login_required

from guardian.shortcuts import assign_perm, get_objects_for_user, get_users_with_perms

# Create your views here.

# ========================= Admin Panel views ==============================

# --------------------------------University-----------------------------------
# --------------------------------Courses-----------------------------------


@login_required
def dashboard(request):
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=request.user)
    univ = None
    if user.is_staff:
        univ = TblUniversity.objects.all()
    elif user.groups.filter(name='director').exists() or user.groups.filter(name='principal').exists() or user.groups.filter(name='hod').exists() or user.groups.filter(name='faculty').exists():
        if get_objects_for_user(request.user, 'University.view_tbluniversity').exists():
            univ = get_objects_for_user(request.user, 'University.view_tbluniversity')
    return render(request, 'dashboard.html',
                  {'Users': request.user,
                   'admin': User_Admin,
                   'univ': univ,
                   'is_director': request.user.groups.filter(name='director').exists(),
                   'is_principal': request.user.groups.filter(name='principal').exists(),
                   'is_hod': request.user.groups.filter(name='hod').exists(),
                   'is_faculty': request.user.groups.filter(name='faculty').exists(),
                   })


@login_required
def add_university(request):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    # PERMISSION TO INSERT
    if not user.has_perm('University.add_tbluniversity'):
        return redirect('dashboard')
    if request.POST:
        univ1 = request.POST['univ1']
        unique_no = request.POST['uno1']
        add1 = request.POST['add1']
        city = request.POST['city1']
        state = request.POST['state1']
        Add_Univ = TblUniversity()
        Add_Univ.university_name = univ1
        Add_Univ.university_unique_num = unique_no
        Add_Univ.university_address = add1
        Add_Univ.university_city = city
        Add_Univ.university_state = state
        Add_Univ.save()
        return redirect('dashboard')
    return render(request, 'add_university.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err})


@login_required
def update_university(request, key):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    Update_Univ = TblUniversity.objects.get(id=key)
    # PERMISSION TO UPDATE
    if user.has_perm('University.change_tbluniversity') or user.has_perm('University.change_tbluniversity', Update_Univ):
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
        return render(request, 'update_university.html',
                      {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                       'Update_Univ': Update_Univ})
    return redirect('dashboard')


@login_required
def delete_university(request, key):
    user = request.user
    Del_Univ = TblUniversity.objects.get(id=key)
    # PERMISSION TO DELETE
    if user.has_perm('University.delete_tbluniversity'):
        Del_Univ.delete()
    return redirect('dashboard')


# --------------------------------Institute-----------------------------------
@login_required
def view_institute(request, key):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    institute = TblInstitutes.objects.filter(university_id=key)
    parent_univ = TblUniversity.objects.get(id=key)
    # PERMISSION TO VIEW
    if not user.has_perm('University.view_tblinstitutes'):
        return redirect('dashboard')
    return render(request, 'institute.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'error': err,
                   'institute': institute, 'parent_univ': parent_univ})


@login_required
def add_institute(request, key):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    parent_univ = TblUniversity.objects.get(id=key)

    # PERMISSION TO INSERT
    if not user.has_perm('University.add_tblinstitutes'):
        return redirect('view_institute', key=parent_univ.id)

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
        try:
            director = get_users_with_perms(parent_univ).get(groups__name='director')
            assign_perm('University.view_tblinstitutes', director, Add_Institute)
            assign_perm('University.change_tblinstitutes', director, Add_Institute)
            assign_perm('University.delete_tblinstitutes', director, Add_Institute)
        except Exception:
            messages.warning(request, 'Director of this institute was not found.' + '\n'
                             'View, Change and Delete permissions were not assigned')
        return redirect('view_institute', key=parent_univ.id)

    return render(request, 'add_institute.html',
                  {
                      'Users': user,
                      'admin': User_Admin,
                      'univ': univ,
                      'error': err,
                      'parent_univ': parent_univ})


@login_required
def update_institute(request, key):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    Update_Institute = TblInstitutes.objects.get(id=key)
    parent_univ = Update_Institute.university_id

    # PERMISSION TO UPDATE
    if not user.has_perm('University.change_tblinstitutes'):
        return redirect('view_institute', key=parent_univ.id)

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
        return redirect('view_institute', key=parent_univ.id)

    return render(request, 'update_institute.html',
                  {'Users': user,
                   'admin': User_Admin,
                   'univ': univ,
                   'error': err,
                   'update_institute': Update_Institute,
                   'parent_univ': parent_univ})


@login_required
def delete_institute(request, key):
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    Del_Institute = TblInstitutes.objects.get(id=key)
    parent_univ = Del_Institute.university_id

    # PERMISSION TO DELETE
    if not user.has_perm('University.delete_tblinstitutes'):
        return redirect('view_institute', key=parent_univ.id)
    else:
        Del_Institute.delete()
        return redirect('view_institute', key=parent_univ.id)


# --------------------------------Department-----------------------------------


@login_required
def view_department(request, key):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    department = TblDepartments.objects.filter(institute_id=key)
    parent_institute = TblInstitutes.objects.get(id=key)

    # PERMISSION TO VIEW
    if not user.has_perm('University.view_tbldepartments'):
        return redirect('dashboard')

    return render(request, 'department.html',
                  {'Users': user,
                   'admin': User_Admin,
                   'univ': univ,
                   'error': err,
                   'department': department,
                   'parent_institute': parent_institute})


@login_required
def add_department(request, key):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    parent_institute = TblInstitutes.objects.get(id=key)

    # PERMISSION TO INSERT
    if not user.has_perm('University.add_tbldepartments'):
        return redirect('view_department', key=parent_institute.id)

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
        try:
            director = get_users_with_perms(parent_institute).get(groups__name='director')
            assign_perm('University.view_tbldepartments', director, Add_Department)
            assign_perm('University.change_tbldepartments', director, Add_Department)
            assign_perm('University.delete_tbldepartments', director, Add_Department)
        except Exception:
            messages.warning(request, 'Unable to find principal of ' + parent_institute.university_id.university_name + '\n'
                             'View, Change and Delete permissions were not assigned')
        try:
            principal = get_users_with_perms(parent_institute).get(groups__name='principal')
            assign_perm('University.view_tbldepartments', principal, Add_Department)
            assign_perm('University.change_tbldepartments', principal, Add_Department)
            assign_perm('University.delete_tbldepartments', principal, Add_Department)
        except Exception:
            messages.warning(request, 'Unable to find principal of ' + parent_institute.institute_name + '\n'
                             'View, Change and Delete permissions were not assigned')
        return redirect('view_department', key=parent_institute.id)

    return render(request, 'add_department.html',
                  {'Users': user,
                   'admin': User_Admin,
                   'univ': univ,
                   'error': err,
                   'parent_institute': parent_institute})


@login_required
def update_department(request, key):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    Update_Department = TblDepartments.objects.get(id=key)
    parent_institute = Update_Department.institute_id

    # PERMISSION TO UPDATE
    if not user.has_perm('University.change_tbldepartments'):
        return redirect('view_department', key=parent_institute.id)

    if request.POST:
        dept1 = request.POST['dept1']
        contactperson1 = request.POST['person1']
        cno1 = request.POST['cno1']
        Update_Department.department_name = dept1
        Update_Department.department_contact_person = contactperson1
        Update_Department.department_contact = cno1
        Update_Department.save()
        return redirect('view_department', key=parent_institute.id)

    return render(request, 'update_department.html',
                  {'Users': user,
                   'admin': User_Admin,
                   'univ': univ,
                   'error': err,
                   'update_department': Update_Department,
                   'parent_institute': parent_institute})


@login_required
def delete_department(request, key):
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    Del_Department = TblDepartments.objects.get(id=key)
    parent_institute = Del_Department.institute_id

    # PERMISSION TO DELETE
    if not user.has_perm('University.delete_tbldepartments'):
        return redirect('view_department', key=parent_institute.id)
    else:
        Del_Department.delete()
        return redirect('view_department', key=parent_institute.id)


# --------------------------------Course-----------------------------------


@login_required
def view_course(request, key):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    course = TblCourses.objects.filter(department_id=key)
    parent_department = TblDepartments.objects.get(id=key)

    # PERMISSION TO VIEW
    if not user.has_perm('University.view_tblcourses'):
        return redirect('dashboard')

    return render(request, 'course.html',
                  {'Users': user,
                   'admin': User_Admin,
                   'univ': univ,
                   'error': err,
                   'course': course,
                   'parent_department': parent_department})


@login_required
def add_course(request, key):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    parent_department = TblDepartments.objects.get(id=key)

    # PERMISSION TO INSERT
    if not user.has_perm('University.add_tblcourses'):
        return redirect('view_course', key=parent_department.id)

    if request.POST:
        name1 = request.POST['nm1']
        code1 = request.POST['code1']
        syllabus1 = request.POST['syllabus1']
        Add_Course = TblCourses()
        Add_Course.department_id = parent_department
        Add_Course.courses_name = name1
        Add_Course.courses_code = code1
        Add_Course.courses_syllabus = syllabus1
        Add_Course.save()
        try:
            director = get_users_with_perms(parent_department).get(groups__name='director')
            assign_perm('University.view_tblcourses', director, Add_Course)
            assign_perm('University.change_tblcourses', director, Add_Course)
            assign_perm('University.delete_tblcourses', director, Add_Course)
        except Exception:
            messages.warning(request, 'Unable to find principal of ' + parent_department.institute_id.university_id.university_name + '\n'
                             'View, Change and Delete permissions were not assigned')
        try:
            principal = get_users_with_perms(parent_department).get(groups__name='principal')
            assign_perm('University.view_tblcourses', principal, Add_Course)
            assign_perm('University.change_tblcourses', principal, Add_Course)
            assign_perm('University.delete_tblcourses', principal, Add_Course)
        except Exception:
            messages.warning(request, 'Unable to find principal of ' + parent_department.institute_id.institute_name + '\n'
                             'View, Change and Delete permissions were not assigned')
        try:
            hod = get_users_with_perms(parent_department).get(groups__name='hod')
            assign_perm('University.view_tblcourses', hod, Add_Course)
            assign_perm('University.change_tblcourses', hod, Add_Course)
            assign_perm('University.delete_tblcourses', hod, Add_Course)
        except Exception:
            messages.warning(request, 'Unable to find HOD of ' + parent_department.department_name + '\n'
                             'View, Change and Delete permissions were not assigned')
        return redirect('view_course', key=parent_department.id)
    return render(request, 'add_course.html',
                  {'Users': user,
                   'admin': User_Admin,
                   'univ': univ,
                   'error': err,
                   'parent_department': parent_department})


@login_required
def update_course(request, key):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    univ = TblUniversity.objects.all()
    Update_Course = TblCourses.objects.get(id=key)
    parent_department = Update_Course.department_id
    # PERMISSION TO UPDATE
    if not user.has_perm('University.add_tblcourses'):
        return redirect('view_course', key=parent_department.id)
    if request.POST:
        name1 = request.POST['nm1']
        code1 = request.POST['code1']
        syllabus1 = request.POST['syllabus1']

        Update_Course.courses_name = name1
        Update_Course.courses_code = code1
        Update_Course.courses_syllabus = syllabus1
        Update_Course.save()
        return redirect('view_course', key=parent_department.id)
    return render(request, 'update_course.html',
                  {'Users': user,
                   'admin': User_Admin,
                   'univ': univ,
                   'error': err,
                   'update_course': Update_Course,
                   'parent_department': parent_department})


@login_required
def delete_course(request, key):
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    Del_Course = TblCourses.objects.get(id=key)
    parent_department = Del_Course.department_id

    # PERMISSION TO DELETE
    if not user.has_perm('University.delete_tblinstitutes'):
        return redirect('view_course', key=parent_department.id)
    else:
        Del_Course.delete()
        return redirect('view_course', key=parent_department.id)
