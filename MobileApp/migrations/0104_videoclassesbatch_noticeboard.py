# Generated by Django 4.1.5 on 2023-09-26 04:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0065_newquestionpool_dtp_edit'),
        ('course', '0054_alter_batch_photo_alter_branch_photo_and_more'),
        ('MobileApp', '0103_libraryfine_historicallibraryfine'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoClassesBatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_status', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.batch')),
                ('module', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.module')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.subject')),
                ('subtopic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.subtopic')),
                ('topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.topic')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.studiovideo')),
            ],
        ),
        migrations.CreateModel(
            name='NoticeBoard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('content', models.TextField()),
                ('is_status', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('batch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.batch')),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.branch')),
            ],
        ),
    ]