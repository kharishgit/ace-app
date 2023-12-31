# Generated by Django 4.1.5 on 2023-05-22 11:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0025_facultyattendence_current_salary_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, default=django.utils.timezone.now)),
                ('package_name', models.CharField(max_length=255)),
                ('duration', models.IntegerField(null=True)),
                ('price', models.IntegerField(null=True)),
                ('offer_price', models.IntegerField(null=True)),
                ('description', models.TextField(null=True)),
                ('benefits', models.TextField(null=True)),
                ('status', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course')),
            ],
        ),
    ]
