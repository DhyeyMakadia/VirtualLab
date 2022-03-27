from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group

from University.models import TblUniversity, TblInstitutes, TblDepartments, TblCourses


def give_admin_permission(user):
    try:
        admin_group = Group.objects.get(name='admin')
    except Group.DoesNotExist:
        raise Group.DoesNotExist
    user.groups.add(admin_group)


def give_director_permission(user):
    try:
        director_group = Group.objects.get(name='director')
    except Group.DoesNotExist:
        raise Group.DoesNotExist
    user.groups.add(director_group)


def give_principal_permission(user):
    try:
        principal_group = Group.objects.get(name='principal')
    except Group.DoesNotExist:
        raise Group.DoesNotExist
    user.groups.add(principal_group)


def give_hod_permission(user):
    try:
        hod_group = Group.objects.get(name='hod')
    except Group.DoesNotExist:
        raise Group.DoesNotExist
    user.groups.add(hod_group)


def give_faculty_permission(user):
    try:
        faculty_group = Group.objects.get(name='faculty')
    except Group.DoesNotExist:
        raise Group.DoesNotExist
    user.groups.add(faculty_group)


def give_permission_for_model(user, perm, model):
    content_type = ContentType.objects.get_for_model(model)
    try:
        permission = Permission.objects.get(codename=perm, content_type=content_type)
    except Permission.DoesNotExist:
        raise Permission.DoesNotExist
    user.user_permissions.add(permission)
    user.save()


def remove_permission(user, perm, model):
    content_type = ContentType.objects.get_for_model(model)
    try:
        permission = Permission.objects.get(codename=perm, content_type=content_type)
    except Permission.DoesNotExist:
        raise Permission.DoesNotExist
    user.user_permissions.remove(permission)
    user.save()
