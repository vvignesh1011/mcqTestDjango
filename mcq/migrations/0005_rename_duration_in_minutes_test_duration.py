# Generated by Django 4.2.3 on 2023-08-04 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mcq', '0004_answersheet_duration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test',
            old_name='duration in minutes',
            new_name='duration',
        ),
    ]