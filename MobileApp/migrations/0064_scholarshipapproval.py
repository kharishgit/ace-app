# Generated by Django 4.1.5 on 2023-08-10 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0027_deliveryaddress'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MobileApp', '0063_scholarshiptype_status_storiescategory_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScholarshipApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved_on', models.DateField(null=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('approved_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
                ('type', models.ManyToManyField(to='MobileApp.scholarshiptype')),
            ],
        ),
    ]