# Generated by Django 4.1.5 on 2023-08-23 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0051_user_is_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='studiovideo',
            name='intro',
            field=models.BooleanField(default=False),
        ),
    ]
