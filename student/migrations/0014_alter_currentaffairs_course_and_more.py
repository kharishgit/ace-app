# Generated by Django 4.1.5 on 2023-06-17 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0032_facultyattendence_status'),
        ('student', '0013_currentaffairs_videolength_currentaffairs_vimeoid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentaffairs',
            name='course',
            field=models.ManyToManyField(blank=True, to='course.course'),
        ),
        migrations.AlterField(
            model_name='publications',
            name='course',
            field=models.ManyToManyField(blank=True, to='course.course'),
        ),
    ]
