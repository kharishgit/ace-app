# Generated by Django 4.1.5 on 2023-03-30 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlineStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.CharField(max_length=10, unique=True)),
                ('otp', models.CharField(max_length=6, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('exam_number', models.IntegerField(blank=True, null=True)),
                ('admission_number', models.IntegerField(blank=True, null=True)),
                ('father_name', models.CharField(blank=True, max_length=30)),
                ('guardian_name', models.CharField(blank=True, max_length=30)),
                ('dob', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('marital_status', models.CharField(blank=True, choices=[('1', 'Single'), ('2', 'Married')], max_length=1)),
                ('religion', models.CharField(blank=True, max_length=20)),
                ('caste', models.CharField(blank=True, max_length=20)),
                ('address', models.TextField(blank=True)),
                ('pincode', models.IntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('mobile', models.CharField(max_length=10, unique=True)),
                ('qualification', models.CharField(blank=True, max_length=30)),
                ('is_active', models.BooleanField(default=False)),
                ('otp', models.CharField(blank=True, max_length=6, null=True)),
                ('admission_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('batch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.batch')),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.branch')),
            ],
        ),
    ]
