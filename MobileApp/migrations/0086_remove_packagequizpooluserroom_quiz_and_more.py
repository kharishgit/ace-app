# Generated by Django 4.1.5 on 2023-09-11 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0056_studiovideo_thumbnail'),
        ('MobileApp', '0085_packagequizpool_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='packagequizpooluserroom',
            name='quiz',
        ),
        migrations.AddField(
            model_name='packagequizpooluserroom',
            name='Exampaper_package',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MobileApp.exampaperpackage'),
        ),
        migrations.AddField(
            model_name='packagequizpooluserroom',
            name='count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='packagequizpooluserroom',
            name='question_paper',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.questionpaper'),
        ),
        migrations.AddField(
            model_name='packagequizpooluserroom',
            name='video_package',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MobileApp.vediopackage'),
        ),
        migrations.DeleteModel(
            name='PackageQuizPool',
        ),
    ]