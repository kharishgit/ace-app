# Generated by Django 4.1.5 on 2023-08-23 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0028_student_scholarship'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentapplicationoffline',
            name='photo',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]