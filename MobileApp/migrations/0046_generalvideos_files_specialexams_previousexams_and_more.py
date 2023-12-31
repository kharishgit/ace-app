# Generated by Django 4.1.5 on 2023-07-27 04:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0043_incentives_types'),
        ('course', '0048_alter_facultyattendence_current_salary_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MobileApp', '0045_vediometerialandquestions_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalvideos',
            name='files',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.CreateModel(
            name='SpecialExams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=255)),
                ('imagetitle', models.CharField(max_length=255, null=True)),
                ('thumbnail', models.ImageField(upload_to='')),
                ('status', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('exampaper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.questionpaper')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.faculty')),
            ],
        ),
        migrations.CreateModel(
            name='PreviousExams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=255)),
                ('imagetitle', models.CharField(max_length=255, null=True)),
                ('thumbnail', models.ImageField(upload_to='')),
                ('status', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='course.course')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('exampaper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.questionpaper')),
            ],
        ),
        migrations.CreateModel(
            name='DailyExams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=255)),
                ('imagetitle', models.CharField(max_length=255, null=True)),
                ('thumbnail', models.ImageField(upload_to='')),
                ('status', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('exampaper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.questionpaper')),
                ('level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='course.level')),
            ],
        ),
    ]
