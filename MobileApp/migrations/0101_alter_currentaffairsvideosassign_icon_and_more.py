# Generated by Django 4.1.5 on 2023-09-21 08:42

from django.db import migrations, models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('MobileApp', '0100_alter_currentaffairsvideosassign_icon_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentaffairsvideosassign',
            name='icon',
            field=models.ImageField(storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='dailyexams',
            name='banner',
            field=models.ImageField(null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='dailyexams',
            name='thumbnail',
            field=models.ImageField(storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='exampaperpackage',
            name='banner',
            field=models.ImageField(null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='exampaperpackage',
            name='thumbnail',
            field=models.ImageField(storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='generalvideos',
            name='thumbnails',
            field=models.ImageField(null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='groups',
            name='icon',
            field=models.ImageField(null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='previousexams',
            name='banner',
            field=models.ImageField(null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='previousexams',
            name='thumbnail',
            field=models.ImageField(storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='questionbook',
            name='icon',
            field=models.ImageField(null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='specialexams',
            name='banner',
            field=models.ImageField(null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='specialexams',
            name='thumbnail',
            field=models.ImageField(storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='stories',
            name='image',
            field=models.ImageField(null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='storiescategory',
            name='image',
            field=models.ImageField(null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='studymaterial',
            name='icon',
            field=models.ImageField(null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='successstories',
            name='icon',
            field=models.ImageField(storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='vediometerialandquestions',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='vediopackage',
            name='banner',
            field=models.ImageField(null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='vediopackage',
            name='image',
            field=models.ImageField(storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/'),
        ),
    ]
