# Generated by Django 4.0.4 on 2022-06-01 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartmentdealing',
            name='dabang',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='apartmentdealing',
            name='elevator',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='apartmentdealing',
            name='empty',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='apartmentdealing',
            name='loan',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='apartmentdealing',
            name='naver',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='apartmentdealing',
            name='parking',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='apartmentdealing',
            name='peterpan',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='apartmentdealing',
            name='zicbang',
            field=models.BooleanField(null=True),
        ),
    ]