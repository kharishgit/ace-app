# Generated by Django 4.1.5 on 2023-09-28 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0054_alter_batch_photo_alter_branch_photo_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MobileApp', '0105_alter_comments_comment_assign_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='onlinecoursepackage',
            name='created_at',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='onlinecoursepackage',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='onlinecoursepackage',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='OnlineCourseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, default=django.utils.timezone.now)),
                ('day', models.IntegerField()),
                ('is_delete', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('onlinecourse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MobileApp.onlinecoursepackage')),
                ('topics', models.ManyToManyField(to='course.topic')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalOnlineCoursePackage',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, default=django.utils.timezone.now, null=True)),
                ('name', models.CharField(max_length=225)),
                ('descriptions', models.TextField()),
                ('validity', models.DurationField()),
                ('benifites', models.TextField()),
                ('prize', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('strike_prize', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('payment_type', models.CharField(choices=[('fullpayment', 'fullpayment'), ('installment', 'installment')], default='fullpayment', max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('course', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='course.course')),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical online course package',
                'verbose_name_plural': 'historical online course packages',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalOnlineCourseOrder',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, default=django.utils.timezone.now)),
                ('day', models.IntegerField()),
                ('is_delete', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('onlinecourse', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='MobileApp.onlinecoursepackage')),
            ],
            options={
                'verbose_name': 'historical online course order',
                'verbose_name_plural': 'historical online course orders',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]