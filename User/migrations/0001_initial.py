# Generated by Django 3.2.3 on 2022-02-10 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('University', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='TblAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_name', models.CharField(blank=True, default='Admin', max_length=50, null=True, verbose_name='Admin Name')),
                ('admin_contact_number', models.PositiveIntegerField(default=0, verbose_name='Contact No.')),
                ('admin_image', models.ImageField(blank=True, default='', max_length=200, null=True, upload_to='User/Admin_Images')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('is_delete', models.BooleanField(default=False, verbose_name='is_delete')),
                ('insert_date_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date_time', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(db_index=True, max_length=60, null=True, unique=True, verbose_name='email')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TblUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Username')),
                ('user_mobile_number', models.PositiveIntegerField(default=0, verbose_name='Mobile No.')),
                ('user_enrollment_number', models.PositiveIntegerField(default=0, verbose_name='Enrollment No.')),
                ('is_approved', models.BooleanField(default=False)),
                ('is_verified_email', models.BooleanField(default=False, verbose_name='is_verified_email')),
                ('is_verified_mobile', models.BooleanField(default=False, verbose_name='is_verified_mobile')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('is_delete', models.BooleanField(default=False, verbose_name='is_delete')),
                ('insert_date_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date_time', models.DateTimeField(auto_now=True, null=True)),
                ('user_device_id', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='user_device_id')),
                ('account_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('department_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='users_department_id', to='University.tbldepartments')),
                ('institute_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='users_institute_id', to='University.tblinstitutes')),
            ],
        ),
        migrations.CreateModel(
            name='TblPermissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, default='Admin', max_length=100, null=True, verbose_name='Role')),
                ('can_view', models.BooleanField(default=True, verbose_name='can_view')),
                ('can_edit', models.BooleanField(default=False, verbose_name='can_edit')),
                ('can_insert', models.BooleanField(default=False, verbose_name='can_insert')),
                ('can_delete', models.BooleanField(default=False, verbose_name='can_delete')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('is_delete', models.BooleanField(default=False, verbose_name='is_delete')),
                ('insert_date_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date_time', models.DateTimeField(auto_now=True, null=True)),
                ('admin_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='permissions_admin_id', to='User.tbladmin')),
                ('allowed_courses', models.ManyToManyField(to='University.TblCourses')),
                ('allowed_department', models.ManyToManyField(to='University.TblDepartments')),
                ('allowed_institute', models.ManyToManyField(to='University.TblInstitutes')),
                ('allowed_university', models.ManyToManyField(to='University.TblUniversity')),
            ],
        ),
        migrations.AddField(
            model_name='tbladmin',
            name='account_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tbladmin',
            name='department_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='admins_department_id', to='University.tbldepartments'),
        ),
        migrations.AddField(
            model_name='tbladmin',
            name='institute_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='admins_institute_id', to='University.tblinstitutes'),
        ),
    ]
