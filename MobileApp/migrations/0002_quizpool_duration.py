# Generated by Django 4.1.5 on 2023-06-16 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MobileApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizpool',
            name='duration',
            field=models.IntegerField(default=5),
        ),
    ]
