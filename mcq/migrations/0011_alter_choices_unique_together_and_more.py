# Generated by Django 4.2.3 on 2023-07-16 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mcq', '0010_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='choices',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='choices',
            name='question',
        ),
        migrations.RemoveField(
            model_name='question',
            name='test',
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='Choices',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.DeleteModel(
            name='TestTaker',
        ),
    ]
