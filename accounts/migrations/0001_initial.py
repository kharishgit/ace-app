# Generated by Django 4.1.5 on 2023-03-30 15:47

import accounts.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('mobile', models.CharField(max_length=10, null=True, unique=True)),
                ('password', models.CharField(max_length=220)),
                ('joined_date', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_faculty', models.BooleanField(default=False)),
                ('is_roleuser', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Declaration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('declaration', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inst_name', models.CharField(max_length=100, null=True)),
                ('years', models.IntegerField(null=True)),
                ('designation', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, null=True)),
                ('address', models.TextField(null=True)),
                ('identity_card', models.FileField(null=True, upload_to='')),
                ('photo', models.ImageField(null=True, upload_to='')),
                ('resume', models.FileField(null=True, upload_to='')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('district', models.CharField(max_length=255, null=True)),
                ('whatsapp_contact_number', models.CharField(max_length=10, null=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('qualification', models.CharField(max_length=255, null=True)),
                ('modeofclasschoice', models.CharField(blank=True, choices=[('1', 'Offline'), ('2', 'Online'), ('3', 'Both')], max_length=1, null=True)),
                ('experiance_link', models.URLField(blank=True, null=True)),
                ('pincode', models.IntegerField(null=True)),
                ('joined_date', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_blocked', models.BooleanField(default=False)),
                ('blockreason', models.TextField(blank=True, null=True)),
                ('is_rejected', models.BooleanField(default=False)),
                ('rejectreason', models.TextField(blank=True, null=True)),
                ('inhouse_fac', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty_Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.CharField(max_length=6)),
                ('fixed_salary', models.CharField(default=None, max_length=7, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FacultyCourseAddition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_approved', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('blocked', 'Blocked')], default='pending', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_faculty', models.CharField(blank=True, max_length=255, null=True)),
                ('file', models.FileField(storage=accounts.models.S3Storage(), upload_to='materials/', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
            ],
        ),
        migrations.CreateModel(
            name='MaterialUploadSupport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_uploaded', models.BooleanField(default=False)),
                ('file', models.FileField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permissions', models.JSONField(default=accounts.models.get_default)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=255)),
                ('option_1', models.CharField(max_length=255)),
                ('option_2', models.CharField(max_length=255)),
                ('option_3', models.CharField(max_length=255)),
                ('option_4', models.CharField(max_length=255)),
                ('option_5', models.CharField(blank=True, max_length=255, null=True)),
                ('answer', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionPool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('1', 'Practise test'), ('2', 'Quesstion Paper')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='SalaryFixation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salaryscale', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
