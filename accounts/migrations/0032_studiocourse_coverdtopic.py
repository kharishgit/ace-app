# Generated by Django 4.1.5 on 2023-06-27 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0035_branch_latitude_branch_longitude_and_more'),
        ('accounts', '0031_studiovideo_totalhours_onlinesalary'),
    ]

    operations = [
        migrations.AddField(
            model_name='studiocourse',
            name='coverdtopic',
            field=models.ManyToManyField(blank=True, related_name='covered_topics', to='course.topic'),
        ),
    ]