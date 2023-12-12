# Generated by Django 4.1.5 on 2023-07-31 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MobileApp', '0048_stories_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='stories',
            name='type',
            field=models.CharField(choices=[('IMAGE', 'IMAGE'), ('VIDEO', 'VIDEO')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='stories',
            name='video_file',
            field=models.URLField(null=True),
        ),
    ]