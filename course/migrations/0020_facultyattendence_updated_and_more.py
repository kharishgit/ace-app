# Generated by Django 4.1.5 on 2023-04-29 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0019_branch_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='facultyattendence',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='facultyattendence',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='facultyattendence',
            name='hours',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
