from rest_framework import serializers

from User.models import Account, TblUsers, TblAdmin


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class TblUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblUsers
        fields = ['account_id',
                  'institute_id',
                  'department_id',
                  'user_name',
                  'user_mobile_number',
                  'user_enrollment_number',
                  'is_verified_email',
                  'is_verified_mobile',
                  'is_active',
                  'is_delete',
                  'insert_date_time',
                  'update_date_time',
                  'user_device_id']


class TblAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblAdmin
        fields = ['account_id',
                  'admin_name',
                  'admin_contact_number',
                  'admin_image',
                  'is_active',
                  'is_delete',
                  'insert_date_time',
                  'update_date_time']


# class TblPermissionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TblPermissions
#         fields = ['admin_id',
#                   'role',
#                   'can_view',
#                   'can_edit',
#                   'can_insert',
#                   'can_delete',
#                   'is_active',
#                   'is_delete',
#                   'insert_date_time',
#                   'update_date_time']
