from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Account, TblUsers, TblAdmin, TblPermissions

# Register your models here.


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email', 'is_active', 'is_staff', 'is_admin')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    fieldsets = (
        (None, {'fields': ('email', )}),
        (_('Permissions'), {'fields': ('is_admin', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined',
                                       'groups', 'user_permissions')}),
    )
    readonly_fields = ('last_login', 'date_joined')
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ['email', ]
    search_fields = ('email', )
    ordering = ('email', )


admin.site.register(Account, UserAdmin)


admin.site.register(TblUsers)

@admin.register(TblAdmin)
class TblAdminAdmin(admin.ModelAdmin):
    list_display = ['admin_name','admin_contact_number','is_active','is_delete']

@admin.register(TblPermissions)
class TblPemissionsAdmin(admin.ModelAdmin):
    list_display = ['admin_id','can_view','can_insert','can_edit','can_delete','is_active','is_delete']
