# Generated by Django 4.1.5 on 2023-09-07 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0051_classrooms_timetable_room'),
        ('MobileApp', '0081_purchasedetails_historicalpurchasedetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.category'),
        ),
        migrations.AddField(
            model_name='groups',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.course'),
        ),
        migrations.AddField(
            model_name='groups',
            name='level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.level'),
        ),
        migrations.AlterField(
            model_name='shorts',
            name='video_file',
            field=models.URLField(),
        ),
    ]