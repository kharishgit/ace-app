# Generated by Django 4.1.5 on 2023-06-24 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0033_facultylimitaion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facultylimitaion',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.branch'),
        ),
    ]
