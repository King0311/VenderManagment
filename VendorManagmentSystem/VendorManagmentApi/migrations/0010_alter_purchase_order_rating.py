# Generated by Django 5.0.2 on 2024-05-01 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VendorManagmentApi', '0009_alter_purchase_order_ack_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase_order',
            name='rating',
            field=models.CharField(blank=True, choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)], max_length=50, null=True),
        ),
    ]
