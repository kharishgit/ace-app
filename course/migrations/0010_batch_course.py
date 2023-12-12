# Generated by Django 4.1.5 on 2023-04-13 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0009_remove_batch_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='course.course_batch'),
        ),
    ]