from django.contrib import admin

from University.models import TblUniversity, TblInstitutes, TblDepartments, TblCourses

# Register your models here.

admin.site.register(TblUniversity)
admin.site.register(TblInstitutes)
admin.site.register(TblDepartments)
admin.site.register(TblCourses)
