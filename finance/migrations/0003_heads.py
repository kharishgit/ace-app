# Generated by Django 4.1.5 on 2023-09-13 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_alter_onlineorderpayment_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Heads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('category', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
            ],
        ),
    ]
