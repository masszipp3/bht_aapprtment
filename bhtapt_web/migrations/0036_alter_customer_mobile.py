# Generated by Django 4.1.5 on 2024-03-04 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bhtapt_web', '0035_booking_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
    ]
