# Generated by Django 4.0.4 on 2022-06-07 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0003_remove_contractbase_finished_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contractbase',
            name='due_days',
        ),
    ]
