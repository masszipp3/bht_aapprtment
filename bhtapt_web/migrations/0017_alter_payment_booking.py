# Generated by Django 5.0 on 2023-12-25 10:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bhtapt_web', '0016_alter_transaction_booking_alter_transaction_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='booking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_booking', to='bhtapt_web.booking'),
        ),
    ]
