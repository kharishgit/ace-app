# Generated by Django 4.1.5 on 2023-04-14 10:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_faculty_salary_fixed_salary'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0011_alter_batch_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.IntegerField(choices=[(1, 'One star'), (2, 'Two stars'), (3, 'Three stars'), (4, 'Four stars'), (5, 'Five stars')])),
                ('question1', models.TextField()),
                ('question2', models.TextField(blank=True, null=True)),
                ('question3', models.TextField(blank=True, null=True)),
                ('question4', models.TextField(blank=True, null=True)),
                ('question5', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Review Questions',
            },
        ),
        migrations.AddField(
            model_name='rating',
            name='rate_fac',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.faculty'),
        ),
        migrations.CreateModel(
            name='SpecialHoliday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('batches', models.ManyToManyField(blank=True, to='course.batch')),
                ('branches', models.ManyToManyField(blank=True, to='course.branch')),
                ('levels', models.ManyToManyField(blank=True, to='course.level')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer1', models.TextField()),
                ('answer2', models.TextField(blank=True, null=True)),
                ('answer3', models.TextField(blank=True, null=True)),
                ('answer4', models.TextField(blank=True, null=True)),
                ('answer5', models.TextField(blank=True, null=True)),
                ('review_on', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.timetable')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FacultyRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.IntegerField(choices=[(1, 'One star'), (2, 'Two stars'), (3, 'Three stars'), (4, 'Four stars'), (5, 'Five stars')])),
                ('rating_on', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.faculty')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
