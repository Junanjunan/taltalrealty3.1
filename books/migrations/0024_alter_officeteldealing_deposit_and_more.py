# Generated by Django 4.0.4 on 2022-06-26 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0023_alter_roomdealing_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officeteldealing',
            name='deposit',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='officeteldealing',
            name='month_fee',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
