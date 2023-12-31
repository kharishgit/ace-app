# Generated by Django 4.1.5 on 2023-09-14 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MobileApp', '0093_mobilebanner_is_faculty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment_assign',
            field=models.CharField(choices=[('SHORTS', 'SHORTS'), ('CURRENT_AFFAIRS', 'CURRENT AFFAIRS'), ('STUDY_MATERIALS', 'STUDY MATERIALS'), ('QUESTION_PAPER', 'QUESTION PAPER'), ('VIDEOS', 'VIDEOS'), ('COMMENTS', 'COMMENTS'), ('STORIES', 'STORIES'), ('SUCCESS_STORIES', 'SUCCESS_STORIES'), ('VIDEO_PACKAGE', 'VIDEO_PACKAGE'), ('EXAM_PACKAGE', 'EXAM_PACKAGE')], default='SHORTS', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='likes',
            name='like_assign',
            field=models.CharField(choices=[('SHORTS', 'SHORTS'), ('CURRENT_AFFAIRS', 'CURRENT AFFAIRS'), ('STUDY_MATERIALS', 'STUDY MATERIALS'), ('QUESTION_PAPER', 'QUESTION PAPER'), ('VIDEOS', 'VIDEOS'), ('COMMENTS', 'COMMENTS'), ('STORIES', 'STORIES'), ('SUCCESS_STORIES', 'SUCCESS STORIES'), ('VIDEO_PACKAGE', 'VIDEO_PACKAGE'), ('EXAM_PACKAGE', 'EXAM_PACKAGE')], default='S', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='views',
            name='view_assign',
            field=models.CharField(choices=[('SHORTS', 'SHORTS'), ('CURRENT_AFFAIRS', 'CURRENT AFFAIRS'), ('STUDY_MATERIALS', 'STUDY MATERIALS'), ('QUESTION_PAPER', 'QUESTION PAPER'), ('VIDEOS', 'VIDEOS'), ('COMMENTS', 'COMMENTS'), ('STORIES', 'STORIES'), ('SUCCESS_STORIES', 'SUCCESS STORIES'), ('VIDEO_PACKAGE', 'VIDEO_PACKAGE'), ('EXAM_PACKAGE', 'EXAM_PACKAGE')], default='S', max_length=200, null=True),
        ),
    ]
