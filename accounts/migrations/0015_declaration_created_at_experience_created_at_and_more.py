# Generated by Django 4.1.5 on 2023-05-09 10:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0022_approvals_created_at_batch_created_at_and_more'),
        ('accounts', '0014_alter_questionfile_facultyfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='declaration',
            name='created_at',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='experience',
            name='created_at',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='facultycourseaddition',
            name='created_at',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='material',
            name='created_at',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='newquestionpool',
            name='answerhint',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='newquestionpool',
            name='created_at',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='newquestionpool',
            name='module',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='course.module'),
        ),
        migrations.AddField(
            model_name='permissions',
            name='created_at',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='questionpaper',
            name='created_at',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='questionpaper',
            name='duration',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='questionpaper',
            name='examtype',
            field=models.CharField(choices=[('1', 'Course'), ('2', 'Subject'), ('3', 'Module'), ('4', 'Topic')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='questionpaper',
            name='instruction',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='questionpaper',
            name='module',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='course.module'),
        ),
        migrations.AddField(
            model_name='questionpaper',
            name='negativemark',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='questionpaper',
            name='positivemark',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='role',
            name='created_at',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='salaryfixation',
            name='created_at',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='newquestionpool',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='newquestionpool',
            name='type',
            field=models.CharField(blank=True, choices=[('1', 'Medium'), ('2', 'Simple'), ('3', 'Tough'), ('4', 'All')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='questionpaper',
            name='type',
            field=models.CharField(choices=[('1', 'Free'), ('2', 'Premium')], max_length=1),
        ),
    ]
