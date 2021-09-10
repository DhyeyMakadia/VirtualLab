from rest_framework import serializers
from University.models import TblUniversity, TblInstitutes, TblDepartments, TblCourses


class TblUniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TblUniversity
        fields = ['id',
                  'university_name',
                  'university_unique_num',
                  'university_address',
                  'university_city',
                  'university_state',
                  'is_active',
                  'is_delete',
                  'insert_date_time',
                  'update_date_time']


class TblInstitutesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblInstitutes
        fields = ['id',
                  'university_id',
                  'institute_name',
                  'institute_code',
                  'institute_address',
                  'institute_city',
                  'institute_state',
                  'insert_date_time',
                  'update_date_time']


class TblDepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblDepartments
        fields = ['id',
                  'institute_id',
                  'department_name',
                  'department_contact_person',
                  'department_contact',
                  'is_active',
                  'is_delete',
                  'insert_date_time',
                  'update_date_time']


class TblCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblCourses
        fields = ['id',
                  'department_id',
                  'courses_name',
                  'courses_code',
                  'courses_syllabus',
                  'is_active',
                  'is_delete',
                  'insert_date_time',
                  'update_date_time',]
