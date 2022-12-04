# Generated by Django 4.1.3 on 2022-12-04 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Management',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('deposit', models.IntegerField(blank=True, null=True)),
                ('month_fee', models.FloatField(blank=True, null=True)),
                ('management_fee', models.FloatField(blank=True, null=True)),
                ('parking_fee', models.FloatField(blank=True, null=True)),
                ('contract_day', models.DateField()),
                ('deal_report', models.BooleanField()),
                ('contract_start_day', models.DateField()),
                ('contract_last_day', models.DateField()),
                ('deal_renewal_notice', models.BooleanField()),
                ('deal_renewal_right_usage', models.BooleanField()),
                ('owner_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('tenant_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
