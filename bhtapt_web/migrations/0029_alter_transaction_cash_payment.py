# Generated by Django 5.0 on 2024-01-01 20:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bhtapt_web', '0028_transaction_cash_payment_cash_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='cash_payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions_cash_payment', to='bhtapt_web.cash_payment'),
        ),
    ]
