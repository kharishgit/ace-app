# Generated by Django 4.1.5 on 2023-06-24 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0034_alter_facultylimitaion_branch'),
        ('accounts', '0030_faculty_salary_is_online_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studiovideo',
            name='totalhours',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='OnlineSalary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('payment_status', models.CharField(choices=[('PAID', 'PAID'), ('PARTIAL', 'PARTIAL'), ('PENDING', 'PENDING')], default='PENDING', max_length=100)),
                ('paid_amount', models.CharField(default=0, max_length=10)),
                ('payment_method', models.CharField(choices=[('CASH', 'CASH'), ('UPI', 'UPI'), ('NETBANKING', 'NETBANKING')], default='CASH', max_length=100)),
                ('testimonial', models.TextField(null=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('current_salary', models.CharField(max_length=10, null=True)),
                ('salary_date', models.DateField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('studiocourse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.studiocourse')),
                ('topics_covered', models.ManyToManyField(blank=True, to='course.topic')),
            ],
        ),
    ]