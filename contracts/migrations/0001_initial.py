# Generated by Django 4.0.4 on 2022-08-05 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContractBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('types', models.CharField(choices=[('Deal', '매매'), ('Lease', '임대')], max_length=10)),
                ('address', models.CharField(max_length=100)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('deposit', models.IntegerField(blank=True, null=True)),
                ('month_fee', models.FloatField(blank=True, null=True)),
                ('start_money', models.IntegerField()),
                ('middle_money', models.IntegerField(blank=True, null=True)),
                ('last_money', models.IntegerField()),
                ('start_day', models.DateField()),
                ('middle_day', models.DateField(blank=True, null=True)),
                ('last_day', models.DateField()),
                ('report', models.BooleanField()),
                ('not_finished', models.BooleanField(default=True)),
                ('owner_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('tenant_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
