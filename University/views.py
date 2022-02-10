from django.shortcuts import render, redirect

from User.models import TblAdmin, TblPermissions
from User.decorators import check_authentication

from University.models import TblUniversity, TblInstitutes, TblDepartments, TblCourses

# Create your views here.

# ========================= Admin Panel views ==============================

# --------------------------------University-----------------------------------
# --------------------------------Courses-----------------------------------


@check_authentication
def dashboard(request):
    User_Admin = TblAdmin.objects.get(account_id=request.user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    univ = TblUniversity.objects.all()
    err = str()
    return render(request, 'dashboard.html',
                  {'Users': request.user, 'admin': User_Admin, 'univ': univ, 'permissions': User_Permissions,
                   'error': err})


@check_authentication
def add_university(request):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
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
        Add_Univ.university_unique_num = unique_no
        Add_Univ.university_address = add1
        Add_Univ.university_city = city
        Add_Univ.university_state = state
        Add_Univ.save()
        return redirect('dashboard')
    return render(request, 'add_university.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'permissions': User_Permissions, 'error': err})


@check_authentication
def update_university(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    univ = TblUniversity.objects.all()
    Update_Univ = TblUniversity.objects.get(id=id)
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
    return render(request, 'update_university.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'permissions': User_Permissions, 'error': err,
                   'Update_Univ': Update_Univ})


@check_authentication
def delete_university(request, id):
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)

    # PERMISSION TO DELETE
    if not User_Permissions.can_delete:
        return redirect('dashboard')
    else:
        Del_Univ = TblUniversity.objects.get(id=id)
        Del_Univ.delete()
        return redirect('dashboard')



# --------------------------------Institute-----------------------------------
@check_authentication
def view_institute(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    univ = TblUniversity.objects.all()
    institute = TblInstitutes.objects.filter(university_id=id)
    parent_univ = TblUniversity.objects.get(id=id)
    # PERMISSION TO VIEW
    if not User_Permissions.can_view:
        return redirect('dashboard')

    return render(request, 'institute.html',
                      {'Users': user, 'admin': User_Admin, 'univ': univ, 'permissions': User_Permissions, 'error': err,
                       'institute': institute, 'parent_univ': parent_univ})


@check_authentication
def add_institute(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    univ = TblUniversity.objects.all()
    parent_univ = TblUniversity.objects.get(id=id)

    # PERMISSION TO INSERT
    if not User_Permissions.can_insert:
        return redirect('view_institute', id=parent_univ.id)

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
        return redirect('view_institute', id=parent_univ.id)

    return render(request, 'add_institute.html',
                  {'Users': user, 'admin': User_Admin, 'univ': univ, 'permissions': User_Permissions, 'error': err,
                   'parent_univ': parent_univ})



@check_authentication
def update_institute(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    univ = TblUniversity.objects.all()
    Update_Institute = TblInstitutes.objects.get(id=id)
    parent_univ = Update_Institute.university_id

    # PERMISSION TO UPDATE
    if not User_Permissions.can_edit:
        return redirect('view_institute', id=parent_univ.id)

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
        return redirect('view_institute', id=parent_univ.id)

    return render(request, 'update_institute.html',
                      {'Users': user, 'admin': User_Admin, 'univ': univ, 'permissions': User_Permissions, 'error': err,
                       'update_institute': Update_Institute, 'parent_univ': parent_univ})



@check_authentication
def delete_institute(request, id):
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    Del_Institute = TblInstitutes.objects.get(id=id)
    parent_univ = Del_Institute.university_id

    # PERMISSION TO DELETE
    if not User_Permissions.can_delete:
        return redirect('view_institute', id=parent_univ.id)
    else:
        Del_Institute.delete()
        return redirect('view_institute', id=parent_univ.id)


# --------------------------------Department-----------------------------------


@check_authentication
def view_department(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    univ = TblUniversity.objects.all()
    department = TblDepartments.objects.filter(institute_id=id)
    parent_institute = TblInstitutes.objects.get(id=id)

    # PERMISSION TO VIEW
    if not User_Permissions.can_view:
        return redirect('dashboard')

    return render(request, 'department.html',
                      {'Users': user, 'admin': User_Admin, 'univ': univ, 'permissions': User_Permissions, 'error': err,
                       'department': department, 'parent_institute': parent_institute})


@check_authentication
def add_department(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    univ = TblUniversity.objects.all()
    parent_institute = TblInstitutes.objects.get(id=id)

    # PERMISSION TO INSERT
    if not User_Permissions.can_insert:
        return redirect('view_department', id=parent_institute.id)

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
        return redirect('view_department', id=parent_institute.id)

    return render(request, 'add_department.html',
                      {'Users': user, 'admin': User_Admin, 'univ': univ, 'permissions': User_Permissions, 'error': err,
                       'parent_institute': parent_institute})


@check_authentication
def update_department(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    univ = TblUniversity.objects.all()
    Update_Department = TblDepartments.objects.get(id=id)
    parent_institute = Update_Department.institute_id

    # PERMISSION TO UPDATE
    if not User_Permissions.can_edit:
        return redirect('view_department', id=parent_institute.id)

    if request.POST:
        dept1 = request.POST['dept1']
        contactperson1 = request.POST['person1']
        cno1 = request.POST['cno1']
        Update_Department.department_name = dept1
        Update_Department.department_contact_person = contactperson1
        Update_Department.department_contact = cno1
        Update_Department.save()
        return redirect('view_department', id=parent_institute.id)

    return render(request, 'update_department.html',
                      {'Users': user, 'admin': User_Admin, 'univ': univ, 'permissions': User_Permissions, 'error': err,
                       'update_department': Update_Department, 'parent_institute': parent_institute})


@check_authentication
def delete_department(request, id):
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    Del_Department = TblDepartments.objects.get(id=id)
    parent_institute = Del_Department.institute_id

    # PERMISSION TO DELETE
    if not User_Permissions.can_delete:
        return redirect('view_department', id=parent_institute.id)
    else:
        Del_Department.delete()
        return redirect('view_department', id=parent_institute.id)


# --------------------------------Course-----------------------------------


@check_authentication
def view_course(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    univ = TblUniversity.objects.all()
    course = TblCourses.objects.filter(department_id=id)
    parent_department = TblDepartments.objects.get(id=id)

    # PERMISSION TO VIEW
    if not User_Permissions.can_view:
        return redirect('dashboard')

    return render(request, 'course.html',
                      {'Users': user, 'admin': User_Admin, 'univ': univ, 'permissions': User_Permissions, 'error': err,
                       'course': course, 'parent_department': parent_department})


@check_authentication
def add_course(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    univ = TblUniversity.objects.all()
    parent_department = TblDepartments.objects.get(id=id)

    # PERMISSION TO INSERT
    if not User_Permissions.can_insert:
        return redirect('view_course', id=parent_department.id)

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
        return redirect('view_course', id=parent_department.id)
    return render(request, 'add_course.html',
                      {'Users': user, 'admin': User_Admin, 'univ': univ, 'permissions': User_Permissions, 'error': err,
                       'parent_department': parent_department})


@check_authentication
def update_course(request, id):
    err = str()
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    univ = TblUniversity.objects.all()
    Update_Course = TblCourses.objects.get(id=id)
    parent_department = Update_Course.department_id
    # PERMISSION TO UPDATE
    if not User_Permissions.can_edit:
        return redirect('view_course', id=parent_department.id)
    if request.POST:
        name1 = request.POST['nm1']
        code1 = request.POST['code1']
        syllabus1 = request.POST['syllabus1']

        Update_Course.courses_name = name1
        Update_Course.courses_code = code1
        Update_Course.courses_syllabus = syllabus1
        Update_Course.save()
        return redirect('view_course', id=parent_department.id)
    return render(request, 'update_course.html',
                      {'Users': user, 'admin': User_Admin, 'univ': univ, 'permissions': User_Permissions, 'error': err,
                       'update_course': Update_Course, 'parent_department': parent_department})


@check_authentication
def delete_course(request, id):
    user = request.user
    User_Admin = TblAdmin.objects.get(account_id=user)
    User_Permissions = TblPermissions.objects.get(admin_id=User_Admin)
    Del_Course = TblCourses.objects.get(id=id)
    parent_department = Del_Course.department_id

    # PERMISSION TO DELETE
    if not User_Permissions.can_delete:
        return redirect('view_course', id=parent_department.id)
    else:
        Del_Course.delete()
        return redirect('view_course', id=parent_department.id)
