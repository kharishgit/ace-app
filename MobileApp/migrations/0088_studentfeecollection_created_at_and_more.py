# Generated by Django 4.1.5 on 2023-09-12 03:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0052_historicaltopic_historicalsubtopic_historicalsubject_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MobileApp', '0087_studentattendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentfeecollection',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='studentfeecollection',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='createby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='studentfeecollection',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.CreateModel(
            name='FacultyFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.IntegerField(choices=[(1, 'One star'), (2, 'Two stars'), (3, 'Three stars'), (4, 'Four stars'), (5, 'Five stars')])),
                ('feedback', models.TextField(blank=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('timetable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.timetable')),
            ],
        ),
    ]
