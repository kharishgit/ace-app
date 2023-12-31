# Generated by Django 4.1.5 on 2023-07-05 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0044_review_unique_rateing_limitaion'),
        ('MobileApp', '0009_alter_mobilebanner_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookname', models.CharField(max_length=255)),
                ('icon', models.ImageField(null=True, upload_to='')),
                ('category', models.CharField(max_length=255, null=True)),
                ('book_price', models.CharField(max_length=5)),
                ('discount_price', models.CharField(max_length=5, null=True)),
                ('no_of_pages', models.IntegerField(null=True)),
                ('edition', models.CharField(max_length=100, null=True)),
                ('stock', models.IntegerField(default=1)),
                ('is_online', models.BooleanField(default=False)),
                ('medium', models.CharField(max_length=255, null=True)),
                ('order_count', models.IntegerField(null=True)),
                ('paperback', models.BooleanField(default=True)),
                ('publish_on', models.DateField(null=True)),
                ('description', models.TextField(null=True)),
                ('published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('course', models.ManyToManyField(blank=True, to='course.course')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookname', models.CharField(max_length=255)),
                ('icon', models.ImageField(null=True, upload_to='')),
                ('category', models.CharField(max_length=255, null=True)),
                ('book_price', models.CharField(max_length=5)),
                ('discount_price', models.CharField(max_length=5, null=True)),
                ('no_of_pages', models.IntegerField(null=True)),
                ('edition', models.CharField(max_length=100, null=True)),
                ('stock', models.IntegerField(default=1)),
                ('is_online', models.BooleanField(default=False)),
                ('medium', models.CharField(max_length=255, null=True)),
                ('order_count', models.IntegerField(null=True)),
                ('paperback', models.BooleanField(default=True)),
                ('publish_on', models.DateField(null=True)),
                ('description', models.TextField(null=True)),
                ('published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('course', models.ManyToManyField(blank=True, to='course.course')),
            ],
        ),
    ]
