# Generated by Django 4.1.5 on 2023-07-19 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MobileApp', '0026_generalvideoscategory_generalvideos_priority_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizpool',
            name='question',
        ),
    ]
