# Generated by Django 4.1.5 on 2023-05-10 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0023_timetable_is_combined'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='combined_batch',
            field=models.ManyToManyField(blank=True, related_name='combined_batch', to='course.batch'),
        ),
    ]
