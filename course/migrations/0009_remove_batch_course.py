# Generated by Django 4.1.5 on 2023-04-13 07:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_alter_batch_description_alter_batch_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='batch',
            name='course',
        ),
    ]
