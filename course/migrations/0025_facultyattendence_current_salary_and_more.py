# Generated by Django 4.1.5 on 2023-05-18 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0024_timetable_combined_batch'),
    ]

    operations = [
        migrations.AddField(
            model_name='facultyattendence',
            name='current_salary',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='facultyattendence',
            name='subtopics_covered',
            field=models.ManyToManyField(blank=True, to='course.subtopic_batch'),
        ),
    ]