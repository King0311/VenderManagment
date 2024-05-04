# Generated by Django 5.0.2 on 2024-05-01 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VendorManagmentApi', '0007_alter_purchase_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase_order',
            name='order_date',
        ),
        migrations.AlterField(
            model_name='purchase_order',
            name='rating',
            field=models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=50, null=True),
        ),
    ]
