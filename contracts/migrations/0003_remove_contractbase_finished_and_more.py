# Generated by Django 4.0.4 on 2022-06-07 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contractbase',
            name='finished',
        ),
        migrations.AddField(
            model_name='contractbase',
            name='not_finished',
            field=models.BooleanField(default=True),
        ),
    ]
