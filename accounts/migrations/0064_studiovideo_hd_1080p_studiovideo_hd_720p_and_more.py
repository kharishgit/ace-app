# Generated by Django 4.1.5 on 2023-09-22 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0063_newquestionpool_admin_verify_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studiovideo',
            name='hd_1080p',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studiovideo',
            name='hd_720p',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studiovideo',
            name='sd_240p',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studiovideo',
            name='sd_360p',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studiovideo',
            name='sd_540p',
            field=models.TextField(blank=True, null=True),
        ),
    ]
