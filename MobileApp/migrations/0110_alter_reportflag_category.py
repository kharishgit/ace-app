# Generated by Django 4.1.5 on 2023-09-30 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MobileApp', '0109_historicalonlinecoursepackage_validity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportflag',
            name='category',
            field=models.CharField(choices=[('SEXUAL_CONTENT', 'Sexual content'), ('VIOLENT_OR_REPULSIVE_CONTENT', 'Violent or repulsive content'), ('HATEFUL_OR_ABUSIVE_CONTENT', 'Hateful or abusive content'), ('HARASSMENT_OR_BULLYING', 'Harassment or bullying'), ('HARMFUL_OR_DANGEROUS_ACTS', 'Harmful or dangerous acts'), ('MISINFORMATION', 'Misinformation'), ('CHILD_ABUSE', 'Child abuse'), ('PROMOTES_TERRORISM', 'Promotes terrorism'), ('SPAM_OR_MISLEADING', 'Spam or misleading'), ('LEGAL_ISSUE', 'Legal issue'), ('CAPTIONS_ISSUE', 'Captions issue'), ('NONE_OF_THESE_ARE_MY_ISSUE', 'None of these are my issue')], max_length=200),
        ),
    ]
