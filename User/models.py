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
        user = self.create_user(email=self.normalize_email(email),password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    """    0 means not approved 1 means approved    """
    
    email = models.EmailField('email', max_length=60, unique=True)

    USERNAME_FIELD = 'email'

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class tbl_university(models.Model):
    university_name = models.CharField("University Name", default="", null=True, blank=True, max_length=100)
    university_unique_num = models.CharField("Unique No.",default="",null=True,blank=True,max_length=50)
    university_address = models.TextField("Address",default="",null=True,blank=True)
    university_city = models.CharField("City",default="",blank=True,null=True,max_length=50)
    university_state = models.CharField("State",default="",blank=True,null=True,max_length=50)
    is_active = models.BooleanField("is_active",default=True)
    is_delete = models.BooleanField("is_delete",default=False)
    insert_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return self.university_name

class tbl_institutes(models.Model):
    university_id = models.ForeignKey(tbl_university,related_name="institutes_university_id",on_delete=models.CASCADE,blank=True,null=True)
    institute_name = models.CharField("Institute Name",default="",null=True,blank=True,max_length=100)
    institute_code = models.CharField("Institute Code",default="",null=True,blank=True,max_length=50)
    institute_address = models.TextField("Address",default="",blank=True,null=True)
    institute_city = models.CharField("City",default="",null=True,blank=True,max_length=50)
    institute_state = models.CharField("State",default="",null=True,blank=True,max_length=50)
    insert_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return self.institute_name

class tbl_departments(models.Model):
    institute_id = models.ForeignKey(tbl_institutes,related_name="departments_institute_id",on_delete=models.CASCADE,blank=True,null=True)
    department_name = models.CharField("Department Name",default="",null=True,blank=True,max_length=100)
    department_contact_person = models.CharField("Contact Person",default="",null=True,blank=True,max_length=100)
    department_contact = models.PositiveIntegerField("Contact No.",default=0)
    is_active = models.BooleanField("is_active",default=True)
    is_delete = models.BooleanField("is_delete",default=False)
    insert_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return self.dept_name

class tbl_courses(models.Model):
    department_id = models.ForeignKey(tbl_departments,related_name="courses_department_id",on_delete=models.CASCADE,blank=True,null=True)
    institute_id = models.ForeignKey(tbl_institutes,related_name="courses_institute_id",on_delete=models.CASCADE,blank=True,null=True)
    courses_name = models.CharField("Courses Name",default="",null=True,blank=True,max_length=100)
    courses_code = models.CharField("Courses Code",default="",null=True,blank=True,max_length=100)
    courses_syllabus = models.TextField("Syllabus",default="",blank=True,null=True)
    is_active = models.BooleanField("is_active",default=True)
    is_delete = models.BooleanField("is_delete",default=False)
    insert_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)