# Generated by Django 4.1.5 on 2023-08-02 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0043_incentives_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialreference',
            name='vstatus',
            field=models.BooleanField(default=False),
        ),
    ]