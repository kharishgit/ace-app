# Generated by Django 4.1.5 on 2023-08-22 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0048_alter_facultyattendence_current_salary_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='is_account',
            field=models.BooleanField(default=False),
        ),
    ]
