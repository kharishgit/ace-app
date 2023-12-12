# Generated by Django 4.1.5 on 2023-09-11 12:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0051_classrooms_timetable_room'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalTopic',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=5000)),
                ('description', models.TextField(null=True)),
                ('priority', models.IntegerField(default=0)),
                ('clickStatus', models.BooleanField(default=True)),
                ('photo', models.TextField(blank=True, max_length=100, null=True)),
                ('active', models.BooleanField(default=True)),
                ('day', models.IntegerField(default=None, null=True)),
                ('order', models.IntegerField(null=True)),
                ('time_needed', models.PositiveIntegerField(null=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('module', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='course.module')),
            ],
            options={
                'verbose_name': 'historical topic',
                'verbose_name_plural': 'historical topics',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSubTopic',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=5000)),
                ('description', models.TextField(null=True)),
                ('priority', models.IntegerField(default=0)),
                ('clickStatus', models.BooleanField(default=True)),
                ('time_needed', models.PositiveIntegerField()),
                ('active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('topic', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='course.topic')),
            ],
            options={
                'verbose_name': 'historical sub topic',
                'verbose_name_plural': 'historical sub topics',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSubject',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=5000)),
                ('description', models.TextField(null=True)),
                ('priority', models.IntegerField(default=0)),
                ('clickStatus', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
                ('photo', models.TextField(blank=True, max_length=100, null=True)),
                ('badge', models.TextField(default='Subject')),
                ('is_delete', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('course', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='course.course')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical subject',
                'verbose_name_plural': 'historical subjects',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalModule',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=5000)),
                ('description', models.TextField(null=True)),
                ('priority', models.IntegerField(default=0)),
                ('clickStatus', models.BooleanField(default=True)),
                ('photo', models.TextField(blank=True, max_length=100, null=True)),
                ('badge', models.TextField(default='Module')),
                ('active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='course.subject')),
            ],
            options={
                'verbose_name': 'historical module',
                'verbose_name_plural': 'historical modules',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]