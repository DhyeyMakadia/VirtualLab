# Generated by Django 3.2.3 on 2021-09-16 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appartus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblappartus',
            name='update_date_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='tblappartuscategory',
            name='update_date_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='tblappartussubcategory',
            name='update_date_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]