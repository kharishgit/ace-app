# Generated by Django 4.1.5 on 2023-06-27 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0032_studiocourse_coverdtopic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='convertedmaterials',
            name='batch',
        ),
        migrations.RemoveField(
            model_name='convertedmaterials',
            name='course',
        ),
    ]