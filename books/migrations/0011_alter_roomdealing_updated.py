# Generated by Django 4.0.4 on 2022-06-03 10:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_alter_roomdealing_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomdealing',
            name='updated',
            field=models.DateField(blank=True, default=datetime.date(2022, 6, 3), null=True),
        ),
    ]
