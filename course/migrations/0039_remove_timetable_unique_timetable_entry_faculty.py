# Generated by Django 4.1.5 on 2023-06-30 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0038_timetable_unique_timetable_entry_faculty'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='timetable',
            name='unique_timetable_entry_faculty',
        ),
    ]
