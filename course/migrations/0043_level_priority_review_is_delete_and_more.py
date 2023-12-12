# Generated by Django 4.1.5 on 2023-07-05 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0042_batch_installment_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='priority',
            field=models.IntegerField(null=True, unique=True),
        ),
        migrations.AddField(
            model_name='review',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddConstraint(
            model_name='approvals',
            constraint=models.UniqueConstraint(condition=models.Q(('is_delete', True), _negated=True), fields=('faculty', 'timetable'), name='unique_approval_entry'),
        ),
    ]