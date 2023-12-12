# Generated by Django 4.1.5 on 2023-07-11 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0038_newquestionpool_unique_sub_topic_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty_salary',
            name='exp_salary',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='onlinesalary',
            name='current_salary',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='onlinesalary',
            name='paid_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='salaryfixation',
            name='salaryscale',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]