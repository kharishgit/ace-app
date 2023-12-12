# Generated by Django 4.1.5 on 2023-08-03 15:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MobileApp', '0053_alter_generalvideos_files'),
    ]

    operations = [
        migrations.CreateModel(
            name='Views',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.BigIntegerField()),
                ('view_assign', models.CharField(choices=[('SHORTS', 'SHORTS'), ('CURRENT_AFFAIRS', 'CURRENT AFFAIRS'), ('STUDY_MATERIALS', 'STUDY MATERIALS'), ('QUESTION_PAPER', 'QUESTION PAPER'), ('VIDEOS', 'VIDEOS'), ('COMMENTS', 'COMMENTS'), ('STORIES', 'STORIES')], default='S', max_length=200, null=True)),
                ('view_id', models.BigIntegerField()),
                ('is_delete', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
    ]
