from University.models import TblDepartments, TblInstitutes
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Email required.')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=self.normalize_email(email), password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    """    0 means not approved 1 means approved    """

    email = models.EmailField('email', max_length=60, unique=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True, editable=False)
    last_login = models.DateTimeField('last login', auto_now=True, editable=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class TblUsers(models.Model):
    account_id = models.OneToOneField(Account, on_delete=models.CASCADE)
    institute_id = models.ForeignKey(TblInstitutes, related_name="users_institute_id", on_delete=models.CASCADE,
                                     blank=True, null=True)
    department_id = models.ForeignKey(TblDepartments, related_name="users_department_id", on_delete=models.CASCADE,
                                      blank=True, null=True)
    user_name = models.CharField("Username", default="", blank=True, null=True, max_length=100)
    user_mobile_number = models.PositiveIntegerField("Mobile No.", default=0)
    user_enrollment_number = models.PositiveIntegerField("Enrollment No.", default=0)
    is_approved = models.BooleanField(default=False)
    is_verified_email = models.BooleanField("is_verified_email", default=False)
    is_verified_mobile = models.BooleanField("is_verified_mobile", default=False)
    is_active = models.BooleanField("is_active", default=True)
    is_delete = models.BooleanField("is_delete", default=False)
    insert_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    user_device_id = models.CharField("user_device_id", default="", blank=True, null=True, max_length=100)

    def __str__(self):
        return self.user_name


class TblAdmin(models.Model):
    account_id = models.OneToOneField(Account, on_delete=models.CASCADE)
    admin_name = models.CharField("Admin Name", default="Admin", blank=True, null=True, max_length=50)
    admin_contact_number = models.PositiveIntegerField("Contact No.", default=0)
    admin_image = models.ImageField(upload_to="User/Admin_Images", default="", max_length=200, blank=True, null=True)
    is_active = models.BooleanField("is_active", default=True)
    is_delete = models.BooleanField("is_delete", default=False)
    insert_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.admin_name


class TblPermissions(models.Model):
    admin_id = models.ForeignKey(TblAdmin, related_name="permissions_admin_id", on_delete=models.CASCADE, blank=True,
                                 null=True)
    role = models.CharField("Role",default='Admin',blank=True,null=True,max_length=100)
    can_view = models.BooleanField("can_view", default=True)
    can_edit = models.BooleanField("can_edit", default=False)
    can_insert = models.BooleanField("can_insert", default=False)
    can_delete = models.BooleanField("can_delete", default=False)
    is_active = models.BooleanField("is_active", default=True)
    is_delete = models.BooleanField("is_delete", default=False)
    insert_date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.role