# Generated by Django 4.1.5 on 2023-09-22 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0064_studiovideo_hd_1080p_studiovideo_hd_720p_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='newquestionpool',
            name='dtp_edit',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
