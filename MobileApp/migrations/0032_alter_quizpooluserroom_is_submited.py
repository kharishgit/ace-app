# Generated by Django 4.1.5 on 2023-07-21 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MobileApp', '0031_libraryuser_dues_completed_libraryuser_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizpooluserroom',
            name='is_submited',
            field=models.BooleanField(default=False),
        ),
    ]
