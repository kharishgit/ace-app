# Generated by Django 4.1.5 on 2023-09-21 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0062_alter_faculty_photo_alter_questionpaper_banner_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='newquestionpool',
            name='admin_verify',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='newquestionpool',
            name='dtp_verify',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='newquestionpool',
            name='faculty_reject',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='newquestionpool',
            name='faculty_reject_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='newquestionpool',
            name='faculty_verify',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
