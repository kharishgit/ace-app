# Generated by Django 4.1.5 on 2023-04-05 03:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_alter_batch_description_alter_batch_start_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='batch',
            name='start_time',
        ),
    ]