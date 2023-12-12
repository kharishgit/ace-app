# Generated by Django 4.1.5 on 2023-08-03 09:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0046_remove_materialreference_unique_faculty_topic_material_and_more'),
        ('course', '0048_alter_facultyattendence_current_salary_and_more'),
        ('finance', '0002_alter_onlineorderpayment_product'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MobileApp', '0051_generalvideos_thumbnails'),
    ]

    operations = [
        migrations.CreateModel(
            name='PopularFaculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, default=django.utils.timezone.now)),
                ('priority', models.IntegerField()),
                ('is_delete', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.faculty')),
            ],
        ),
        migrations.CreateModel(
            name='PaidSubscriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, default=django.utils.timezone.now)),
                ('product', models.CharField(choices=[('publication', 'publication'), ('subscription', 'subscription'), ('question_paper', 'question paper'), ('exampackages', 'exampackages'), ('videopackages', 'videopackages')], max_length=50)),
                ('status', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.onlineorderpayment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='popularfaculty',
            constraint=models.UniqueConstraint(condition=models.Q(('is_delete', True), _negated=True), fields=('faculty', 'course'), name='unique_faculty_course'),
        ),
    ]