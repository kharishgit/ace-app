# Generated by Django 4.1.5 on 2023-04-19 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0014_remove_module_unique_module_name_per_subject_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facultyattendence',
            name='description',
        ),
        migrations.RemoveField(
            model_name='facultyattendence',
            name='payed_amnt',
        ),
        migrations.AddField(
            model_name='facultyattendence',
            name='paid_amount',
            field=models.CharField(default=0, max_length=10),
        ),
        migrations.AddField(
            model_name='facultyattendence',
            name='payment_method',
            field=models.CharField(choices=[('CASH', 'CASH'), ('UPI', 'UPI'), ('NETBANKING', 'NETBANKING')], default='CASH', max_length=100),
        ),
        migrations.AlterField(
            model_name='facultyattendence',
            name='payment_done',
            field=models.CharField(choices=[('PAID', 'PAID'), ('PARTIAL', 'PARTIAL'), ('PENDING', 'PENDING')], default='PENDING', max_length=100),
        ),
        migrations.AlterField(
            model_name='facultyattendence',
            name='subtopics_covered',
            field=models.ManyToManyField(to='course.subtopic_batch'),
        ),
    ]
