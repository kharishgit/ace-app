# Generated by Django 4.1.5 on 2023-07-21 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0042_alter_incentives_status_alter_staffincentives_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='incentives',
            name='types',
            field=models.CharField(choices=[('ADMISSION_WISE', 'ADMISSION WISE'), ('SINGLE_PAYMENT_ENCOURAGE_WISE', 'SINGLE PAYMENT ENCOURAGE WISE'), ('PHOTO_COLLECTION ', 'PHOTO COLLECTION '), ('ENQIUREES_WISE', 'ENQIUREES WISE'), ('FOLLOW_UP', 'FOLLOW UP'), ('SOCIAL_MEDIA ', 'SOCIAL MEDIA '), ('CLASS_COMMUNICATION', 'CLASS COMMUNICATION'), ('FEE_COLLECTION_WISE', 'FEE COLLECTION WISE'), ('OTHERS', 'OTHERS')], default='OTHERS', max_length=255),
        ),
    ]
