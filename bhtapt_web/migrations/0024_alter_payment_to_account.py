# Generated by Django 5.0 on 2023-12-31 17:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bhtapt_web', '0023_alter_payment_to_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='to_account',
            field=models.ForeignKey(blank=True, default=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_toaccount', to='bhtapt_web.account'),
        ),
    ]
