# Generated by Django 4.1.5 on 2023-07-15 06:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0048_alter_facultyattendence_current_salary_and_more'),
        ('MobileApp', '0020_remove_cartitem_cart_remove_cartitem_publication_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='books',
            old_name='stock',
            new_name='no_due_days',
        ),
        migrations.AddField(
            model_name='books',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='bookstock',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_assign', models.CharField(choices=[('SHORTS', 'SHORTS'), ('STUDY_MATERIALS', 'STUDY MATERIALS'), ('QUESTION_PAPER', 'QUESTION PAPER'), ('VIDEOS', 'VIDEOS'), ('COMMENTS', 'COMMENTS')], default='S', max_length=200, null=True)),
                ('liked_id', models.BigIntegerField()),
                ('is_delete', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LibraryUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardno', models.CharField(max_length=100)),
                ('book_limit', models.PositiveIntegerField(default=1)),
                ('is_delete', models.BooleanField(default=False)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.branch')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_assign', models.CharField(choices=[('SHORTS', 'SHORTS'), ('STUDY_MATERIALS', 'STUDY MATERIALS'), ('QUESTION_PAPER', 'QUESTION PAPER'), ('VIDEOS', 'VIDEOS'), ('COMMENTS', 'COMMENTS')], default='S', max_length=200, null=True)),
                ('commented_id', models.BigIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookLend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrowed_on', models.DateField()),
                ('duedate', models.DateField()),
                ('returned_on', models.DateField(null=True)),
                ('description', models.TextField(null=True)),
                ('fine', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('lost', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MobileApp.books')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MobileApp.libraryuser')),
            ],
        ),
        migrations.AddConstraint(
            model_name='likes',
            constraint=models.UniqueConstraint(fields=('user', 'like_assign', 'liked_id'), name='unique_like_assign_constraints'),
        ),
        migrations.AddConstraint(
            model_name='comments',
            constraint=models.UniqueConstraint(fields=('user', 'comment_assign'), name='unique_comment_assign_constraints'),
        ),
    ]
