# Generated by Django 4.1.5 on 2023-06-14 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_publications'),
    ]

    operations = [
        migrations.AddField(
            model_name='publications',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
    ]