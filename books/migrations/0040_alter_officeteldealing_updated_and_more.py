# Generated by Django 4.0.4 on 2022-07-08 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0039_alter_officeteldealing_updated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officeteldealing',
            name='updated',
            field=models.DateField(blank=True, default='2022-07-08', null=True),
        ),
        migrations.AlterField(
            model_name='roomdealing',
            name='updated',
            field=models.DateField(blank=True, default='2022-07-08', null=True),
        ),
    ]
