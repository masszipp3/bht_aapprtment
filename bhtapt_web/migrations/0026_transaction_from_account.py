# Generated by Django 5.0 on 2024-01-01 14:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bhtapt_web', '0025_remove_transaction_from_account_payment_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='from_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions_from_account', to='bhtapt_web.account'),
        ),
    ]