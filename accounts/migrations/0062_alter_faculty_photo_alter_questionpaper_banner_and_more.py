# Generated by Django 4.1.5 on 2023-09-21 08:42

from django.db import migrations, models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0061_alter_faculty_photo_alter_questionpaper_banner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='photo',
            field=models.ImageField(null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='questionpaper',
            name='banner',
            field=models.ImageField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='studiovideo',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
    ]
