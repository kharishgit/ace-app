# Generated by Django 4.1.5 on 2023-07-25 09:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MobileApp', '0038_quizpoolanswers_created_at_quizpoolanswers_index_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='storiescategory',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='comments',
            name='comment_assign',
            field=models.CharField(choices=[('SHORTS', 'SHORTS'), ('CURRENT AFFAIRS', 'CURRENT AFFAIRS'), ('STUDY_MATERIALS', 'STUDY MATERIALS'), ('QUESTION_PAPER', 'QUESTION PAPER'), ('VIDEOS', 'VIDEOS'), ('COMMENTS', 'COMMENTS'), ('STORIES', 'STORIES')], default='SHORTS', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='likes',
            name='like_assign',
            field=models.CharField(choices=[('SHORTS', 'SHORTS'), ('CURRENT AFFAIRS', 'CURRENT AFFAIRS'), ('STUDY_MATERIALS', 'STUDY MATERIALS'), ('QUESTION_PAPER', 'QUESTION PAPER'), ('VIDEOS', 'VIDEOS'), ('COMMENTS', 'COMMENTS'), ('STORIES', 'STORIES')], default='S', max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='RecentWatched',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, default=django.utils.timezone.now)),
                ('path', models.CharField(max_length=255)),
                ('is_delete', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
