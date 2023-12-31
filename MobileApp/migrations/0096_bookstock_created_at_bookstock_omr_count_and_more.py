# Generated by Django 4.1.5 on 2023-09-15 06:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MobileApp', '0095_historicalvediopackage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookstock',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='bookstock',
            name='omr_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bookstock',
            name='publication_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bookstock',
            name='questionbank_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bookstock',
            name='studymaterial_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='historicalbookstock',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='historicalbookstock',
            name='omr_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='historicalbookstock',
            name='publication_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='historicalbookstock',
            name='questionbank_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='historicalbookstock',
            name='studymaterial_count',
            field=models.IntegerField(default=0),
        ),
    ]
