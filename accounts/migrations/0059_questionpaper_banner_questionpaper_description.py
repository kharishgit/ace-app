# Generated by Django 4.1.5 on 2023-09-13 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0058_faculty_is_delete_historicalfaculty_is_delete'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionpaper',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='questionpaper',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
