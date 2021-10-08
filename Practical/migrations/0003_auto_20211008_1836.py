# Generated by Django 3.2.3 on 2021-10-08 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Practical', '0002_auto_20210916_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblfixedinputparameter',
            name='practical_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Practical.tblpractical'),
        ),
        migrations.AddField(
            model_name='tblfixedoutputparameter',
            name='practical_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Practical.tblpractical'),
        ),
        migrations.AddField(
            model_name='tblinputparameter',
            name='practical_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Practical.tblpractical'),
        ),
        migrations.AddField(
            model_name='tbloutputparameter',
            name='practical_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Practical.tblpractical'),
        ),
        migrations.AlterField(
            model_name='tblmultiplepracticalimages',
            name='image_path',
            field=models.ImageField(blank=True, default='', max_length=200, null=True, upload_to='', verbose_name='Practical/Multiple-Practical-Images/{practical_id.practical_name}'),
        ),
    ]
