# Generated by Django 4.1.5 on 2023-06-13 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_materialreference_materialupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='facultycourseaddition',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
    ]
