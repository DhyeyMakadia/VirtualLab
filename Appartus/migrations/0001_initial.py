# Generated by Django 3.2.3 on 2022-02-10 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TblAppartusCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appartus_category_name', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Category')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('is_delete', models.BooleanField(default=False, verbose_name='is_delete')),
                ('insert_date_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date_time', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TblAppartusSubcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appartus_subcategory_name', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Sub Category')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('is_delete', models.BooleanField(default=False, verbose_name='is_delete')),
                ('insert_date_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date_time', models.DateTimeField(auto_now=True, null=True)),
                ('appartus_category_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Appartus.tblappartuscategory')),
            ],
        ),
        migrations.CreateModel(
            name='TblAppartus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appartus_name', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Name')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('is_delete', models.BooleanField(default=False, verbose_name='is_delete')),
                ('insert_date_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_date_time', models.DateTimeField(auto_now=True, null=True)),
                ('appartus_category_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Appartus.tblappartuscategory')),
                ('appartus_subcategory_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Appartus.tblappartussubcategory')),
            ],
        ),
    ]
