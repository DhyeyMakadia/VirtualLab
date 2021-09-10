from django.contrib import admin

from .models import Account, TblUsers, TblAdmin, TblRoles, TblPermissions

# Register your models here.

admin.site.register(Account)
admin.site.register(TblUsers)
admin.site.register(TblAdmin)
admin.site.register(TblRoles)
admin.site.register(TblPermissions)
