from rest_framework import serializers

from User.models import Account, TblUsers, TblAdmin, TblRoles, TblPermissions


class RegistrationSerializer(serializers.ModelSerializer):
    # Another password attribute for two time password verification.
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        # Model to be serialized
        model = Account
        # fields of the serializer.
        fields = ['email', 'password', 'password2', 'is_admin']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        # Getting an instance of the model with validated data.
        # university = University.objects.get(id=self.validated_data['university'])
        account = Account(
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        # Checking whether the two passwords match.
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        # Setting the password if two passwords match
        account.set_password(password)
        # Saving the instance to the database, and return it.
        account.save()
        return account


class TblUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblUsers
        fields = ['account_id',
                  'institute_id',
                  'department_id',
                  'user_name',
                  'user_mobile_number',
                  # 'user_email',
                  'user_enrollment_number',
                  # 'user_password',
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
                  # 'admin_email',
                  # 'admin_password',
                  'admin_contact_number',
                  'admin_image',
                  'is_active',
                  'is_delete',
                  'insert_date_time',
                  'update_date_time']


class TblRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblRoles
        fields = ['admin_id',
                  'role_name',
                  'is_active',
                  'is_delete',
                  'insert_date_time',
                  'update_date_time']


class TblPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblPermissions
        fields = ['role_id',
                  'admin_id',
                  'can_view',
                  'can_edit',
                  'can_insert',
                  'can_delete',
                  'is_active',
                  'is_delete',
                  'insert_date_time',
                  'update_date_time']
