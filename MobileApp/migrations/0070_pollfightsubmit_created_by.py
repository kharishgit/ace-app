# Generated by Django 4.1.5 on 2023-08-12 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MobileApp', '0069_pollfightsubmit'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollfightsubmit',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
