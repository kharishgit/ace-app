# Generated by Django 4.1.5 on 2023-07-28 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MobileApp', '0047_currentaffairsvideosassign'),
    ]

    operations = [
        migrations.AddField(
            model_name='stories',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]