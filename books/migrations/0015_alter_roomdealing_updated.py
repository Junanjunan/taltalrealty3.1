# Generated by Django 4.0.4 on 2022-06-06 03:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0014_alter_roomdealing_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomdealing',
            name='updated',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
