# Generated by Django 5.0.2 on 2024-04-29 18:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VendorManagmentApi', '0005_purchase_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor_Performance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('avg_quality_rating', models.FloatField()),
                ('avg_response_time', models.FloatField()),
                ('fulfillment_rate', models.FloatField()),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VendorManagmentApi.vendor')),
            ],
        ),
    ]
