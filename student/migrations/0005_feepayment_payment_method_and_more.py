# Generated by Django 4.1.5 on 2023-05-23 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_alter_feepayment_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='feepayment',
            name='payment_method',
            field=models.CharField(choices=[('CASH', 'CASH'), ('UPI', 'UPI'), ('NETBANKING', 'NETBANKING')], default='CASH', max_length=255),
        ),
        migrations.AlterField(
            model_name='feepayment',
            name='paid_amount',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='feepayment',
            name='pending_amount',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='student',
            name='admission_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='caste',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='father_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='guardian',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='guardian_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='student',
            name='qualification',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='religion',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
