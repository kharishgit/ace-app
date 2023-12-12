# Generated by Django 4.1.5 on 2023-07-27 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0043_incentives_types'),
        ('MobileApp', '0046_generalvideos_files_specialexams_previousexams_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentAffairsVideosAssign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.ImageField(upload_to='')),
                ('published', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=True)),
                ('publish_on', models.DateField(null=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.studiovideo')),
            ],
        ),
    ]