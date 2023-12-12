# Generated by Django 4.1.5 on 2023-07-22 05:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0048_alter_facultyattendence_current_salary_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MobileApp', '0032_alter_quizpooluserroom_is_submited'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('video_file', models.URLField()),
                ('description', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_delete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='StoriesCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='comments',
            name='comment_assign',
            field=models.CharField(choices=[('SHORTS', 'SHORTS'), ('STUDY_MATERIALS', 'STUDY MATERIALS'), ('QUESTION_PAPER', 'QUESTION PAPER'), ('VIDEOS', 'VIDEOS'), ('COMMENTS', 'COMMENTS'), ('STORIES', 'STORIES')], default='SHORTS', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='likes',
            name='like_assign',
            field=models.CharField(choices=[('SHORTS', 'SHORTS'), ('STUDY_MATERIALS', 'STUDY MATERIALS'), ('QUESTION_PAPER', 'QUESTION PAPER'), ('VIDEOS', 'VIDEOS'), ('COMMENTS', 'COMMENTS'), ('STORIES', 'STORIES')], default='S', max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='StoriesWatched',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watched', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('stories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MobileApp.stories')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='stories',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MobileApp.storiescategory'),
        ),
        migrations.AddField(
            model_name='stories',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.level'),
        ),
    ]