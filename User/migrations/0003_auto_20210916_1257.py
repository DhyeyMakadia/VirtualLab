# Generated by Django 3.2.3 on 2021-09-16 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_alter_tblpermissions_can_view'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbladmin',
            name='update_date_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='tblpermissions',
            name='update_date_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='tblroles',
            name='update_date_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='tblusers',
            name='update_date_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]