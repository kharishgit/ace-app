# Generated by Django 4.1.5 on 2023-06-08 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_materialuploads_materialreference'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialreference',
            name='materialupload',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.materialuploads'),
        ),
    ]
