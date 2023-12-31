# Generated by Django 4.1.5 on 2023-07-11 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MobileApp', '0013_questioncategory_bookstock_questionbook_q_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionbook',
            name='admission_time_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='questionbook',
            name='book_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='questionbook',
            name='discount_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='questionbook',
            name='old_student',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='questionbook',
            name='outsider',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='studymaterial',
            name='admission_time_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='studymaterial',
            name='book_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='studymaterial',
            name='discount_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='studymaterial',
            name='old_student',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='studymaterial',
            name='outsider',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
