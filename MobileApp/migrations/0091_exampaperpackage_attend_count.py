# Generated by Django 4.1.5 on 2023-09-13 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MobileApp', '0090_wallet_transactionswallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='exampaperpackage',
            name='attend_count',
            field=models.PositiveIntegerField(default=4, null=True),
        ),
    ]