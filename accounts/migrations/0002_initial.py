# Generated by Django 4.1.5 on 2023-03-30 15:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionpool',
            name='categorys',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.category'),
        ),
        migrations.AddField(
            model_name='questionpool',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course'),
        ),
        migrations.AddField(
            model_name='questionpool',
            name='facultys',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.faculty'),
        ),
        migrations.AddField(
            model_name='questionpool',
            name='levels',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.level'),
        ),
        migrations.AddField(
            model_name='questionpool',
            name='questions',
            field=models.ManyToManyField(to='accounts.question'),
        ),
        migrations.AddField(
            model_name='questionpool',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.topic'),
        ),
        migrations.AddField(
            model_name='permissions',
            name='role',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.role'),
        ),
        migrations.AddField(
            model_name='materialuploadsupport',
            name='faculty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.faculty'),
        ),
        migrations.AddField(
            model_name='materialuploadsupport',
            name='material',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='materialuploadsupport', to='accounts.material'),
        ),
        migrations.AddField(
            model_name='materialuploadsupport',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='course.topic'),
        ),
        migrations.AddField(
            model_name='material',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.category'),
        ),
        migrations.AddField(
            model_name='material',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course'),
        ),
        migrations.AddField(
            model_name='material',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.faculty'),
        ),
        migrations.AddField(
            model_name='material',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.level'),
        ),
        migrations.AddField(
            model_name='material',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.module'),
        ),
        migrations.AddField(
            model_name='material',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.subject'),
        ),
        migrations.AddField(
            model_name='material',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='course.topic'),
        ),
        migrations.AddField(
            model_name='facultycourseaddition',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.category'),
        ),
        migrations.AddField(
            model_name='facultycourseaddition',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course'),
        ),
        migrations.AddField(
            model_name='facultycourseaddition',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.level'),
        ),
        migrations.AddField(
            model_name='facultycourseaddition',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.module'),
        ),
        migrations.AddField(
            model_name='facultycourseaddition',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.subject'),
        ),
        migrations.AddField(
            model_name='facultycourseaddition',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.topic'),
        ),
        migrations.AddField(
            model_name='facultycourseaddition',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='faculty_salary',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.faculty'),
        ),
        migrations.AddField(
            model_name='faculty_salary',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.level'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='expected_salary',
            field=models.ManyToManyField(related_name='faculties', to='accounts.faculty_salary'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_profi', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='experience',
            name='level',
            field=models.ManyToManyField(blank=True, to='course.classlevel'),
        ),
        migrations.AddField(
            model_name='experience',
            name='name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.faculty'),
        ),
    ]