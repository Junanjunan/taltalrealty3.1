# Generated by Django 4.0.4 on 2022-06-27 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0026_alter_storedealing_deposit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officeteldealing',
            name='updated',
            field=models.DateField(blank=True, default='2022-06-27', null=True),
        ),
        migrations.AlterField(
            model_name='roomdealing',
            name='updated',
            field=models.DateField(blank=True, default='2022-06-27', null=True),
        ),
    ]
