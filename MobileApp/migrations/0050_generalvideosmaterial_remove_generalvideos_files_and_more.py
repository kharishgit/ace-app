# Generated by Django 4.1.5 on 2023-08-02 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MobileApp', '0049_stories_type_alter_stories_video_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralVideosMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('files', models.FileField(upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_delete', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='generalvideos',
            name='files',
        ),
        migrations.AddField(
            model_name='generalvideos',
            name='files',
            field=models.ManyToManyField(to='MobileApp.generalvideosmaterial'),
        ),
    ]
