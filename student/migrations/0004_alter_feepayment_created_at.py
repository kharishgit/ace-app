# Generated by Django 4.1.5 on 2023-05-22 13:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_alter_feepayment_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feepayment',
            name='created_at',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
        ),
    ]