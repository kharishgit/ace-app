# Generated by Django 4.1.5 on 2023-08-03 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MobileApp', '0052_popularfaculty_paidsubscriptions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalvideos',
            name='files',
            field=models.ManyToManyField(blank=True, to='MobileApp.generalvideosmaterial'),
        ),
    ]
