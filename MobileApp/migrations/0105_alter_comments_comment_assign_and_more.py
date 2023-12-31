# Generated by Django 4.1.5 on 2023-09-27 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MobileApp', '0104_videoclassesbatch_noticeboard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment_assign',
            field=models.CharField(choices=[('SHORTS', 'SHORTS'), ('CURRENT_AFFAIRS', 'CURRENT AFFAIRS'), ('STUDY_MATERIALS', 'STUDY MATERIALS'), ('QUESTION_PAPER', 'QUESTION PAPER'), ('VIDEOS', 'VIDEOS'), ('COMMENTS', 'COMMENTS'), ('STORIES', 'STORIES'), ('SUCCESS_STORIES', 'SUCCESS_STORIES'), ('VIDEO_PACKAGE', 'VIDEO_PACKAGE'), ('EXAM_PACKAGE', 'EXAM_PACKAGE'), ('CHAT', 'CHAT'), ('ARTICAL', 'ARTICAL')], default='SHORTS', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='likes',
            name='like_assign',
            field=models.CharField(choices=[('SHORTS', 'SHORTS'), ('CURRENT_AFFAIRS', 'CURRENT AFFAIRS'), ('STUDY_MATERIALS', 'STUDY MATERIALS'), ('QUESTION_PAPER', 'QUESTION PAPER'), ('VIDEOS', 'VIDEOS'), ('COMMENTS', 'COMMENTS'), ('STORIES', 'STORIES'), ('SUCCESS_STORIES', 'SUCCESS STORIES'), ('VIDEO_PACKAGE', 'VIDEO_PACKAGE'), ('EXAM_PACKAGE', 'EXAM_PACKAGE'), ('CHAT', 'CHAT'), ('ARTICAL', 'ARTICAL')], default='S', max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='ReportFlag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, default=django.utils.timezone.now)),
                ('report_assign', models.CharField(choices=[('SHORTS', 'SHORTS'), ('CURRENT_AFFAIRS', 'CURRENT AFFAIRS'), ('STUDY_MATERIALS', 'STUDY MATERIALS'), ('QUESTION_PAPER', 'QUESTION PAPER'), ('VIDEOS', 'VIDEOS'), ('COMMENTS', 'COMMENTS'), ('STORIES', 'STORIES'), ('SUCCESS_STORIES', 'SUCCESS STORIES'), ('VIDEO_PACKAGE', 'VIDEO_PACKAGE'), ('EXAM_PACKAGE', 'EXAM_PACKAGE'), ('CHAT', 'CHAT'), ('ARTICAL', 'ARTICAL')], default='S', max_length=200, null=True)),
                ('report_id', models.BigIntegerField()),
                ('category', models.TextField()),
                ('content', models.TextField()),
                ('is_delete', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
