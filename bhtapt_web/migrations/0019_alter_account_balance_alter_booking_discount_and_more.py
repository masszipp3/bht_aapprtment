# Generated by Django 5.0 on 2023-12-31 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bhtapt_web', '0018_alter_transaction_transaction_remark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='booking',
            name='discount',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='booking',
            name='rate',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=15),
        ),
    ]
