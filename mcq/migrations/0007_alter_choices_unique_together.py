# Generated by Django 4.2.3 on 2023-07-16 03:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mcq', '0006_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='choices',
            unique_together={('question', 'name')},
        ),
    ]