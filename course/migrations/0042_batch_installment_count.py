# Generated by Django 4.1.5 on 2023-07-04 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0041_batch_fees_batch_is_special'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='installment_count',
            field=models.IntegerField(default=0),
        ),
    ]
