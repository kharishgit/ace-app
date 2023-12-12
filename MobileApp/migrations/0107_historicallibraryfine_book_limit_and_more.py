# Generated by Django 4.1.5 on 2023-09-29 07:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0055_historicaltopic_video_topic_video'),
        ('MobileApp', '0106_onlinecoursepackage_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicallibraryfine',
            name='book_limit',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='historicallibraryfine',
            name='duedate',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='libraryfine',
            name='book_limit',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='libraryfine',
            name='duedate',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.CreateModel(
            name='ZoomMeetings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=255)),
                ('meeting_id', models.BigIntegerField()),
                ('password', models.CharField(max_length=10)),
                ('image', models.ImageField(storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='dev-aceapp-public', default_acl='public-read', querystring_auth=False), upload_to='Images/')),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('reminder', models.IntegerField(default=0)),
                ('is_delete', models.BooleanField(default=False)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='course.category')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='course.course')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='course.level')),
                ('module', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='course.module')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='course.subject')),
                ('subtopic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='course.subtopic')),
                ('topic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='course.topic')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalZoomMeetings',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=255)),
                ('meeting_id', models.BigIntegerField()),
                ('password', models.CharField(max_length=10)),
                ('image', models.TextField(max_length=100)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('reminder', models.IntegerField(default=0)),
                ('is_delete', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('category', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='course.category')),
                ('course', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='course.course')),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('level', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='course.level')),
                ('module', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='course.module')),
                ('subject', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='course.subject')),
                ('subtopic', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='course.subtopic')),
                ('topic', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='course.topic')),
            ],
            options={
                'verbose_name': 'historical zoom meetings',
                'verbose_name_plural': 'historical zoom meetingss',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]