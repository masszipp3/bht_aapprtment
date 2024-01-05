# Generated by Django 5.0 on 2023-12-31 16:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bhtapt_web', '0021_transaction_from_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='from_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_fromaccount', to='bhtapt_web.account'),
        ),
        migrations.AddField(
            model_name='payment',
            name='to_account',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_toaccount', to='bhtapt_web.account'),
        ),
    ]