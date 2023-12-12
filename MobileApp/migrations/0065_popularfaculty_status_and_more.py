# Generated by Django 4.1.5 on 2023-08-11 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MobileApp', '0064_scholarshipapproval'),
    ]

    operations = [
        migrations.AddField(
            model_name='popularfaculty',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddConstraint(
            model_name='pollfightlobby',
            constraint=models.UniqueConstraint(fields=('user1', 'user2'), name='unique_poll-users'),
        ),
    ]