from django.contrib import admin

from .models import Account, TblUsers, TblAdmin, TblRoles, TblPermissions

# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['email','is_admin','is_active','is_staff','is_superuser']
    
admin.site.register(TblUsers)

@admin.register(TblAdmin)
class TblAdminAdmin(admin.ModelAdmin):
    list_display = ['admin_name','admin_contact_number','is_active','is_delete']
admin.site.register(TblRoles)

@admin.register(TblPermissions)
class TblPemissionsAdmin(admin.ModelAdmin):
    list_display = ['admin_id','can_view','can_insert','can_edit','can_delete','is_active','is_delete']
