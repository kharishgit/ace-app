# Generated by Django 4.1.5 on 2023-04-10 01:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_alter_course_batch_course_alter_module_batch_module_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course_branch'),
        ),
    ]