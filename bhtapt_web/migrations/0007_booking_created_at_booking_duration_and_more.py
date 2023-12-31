# Generated by Django 5.0 on 2023-12-22 13:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bhtapt_web', '0006_alter_room_room_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='duration',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='expected_checkout_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='soft_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='booking',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='room_status',
            field=models.CharField(blank=True, choices=[('1', 'Avaialable'), ('2', 'Booked'), ('3', 'Reserved')], default='1', max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(blank=True, max_length=100, null=True)),
                ('check_in_date', models.DateField()),
                ('check_out_date', models.DateField()),
                ('reservation_status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('soft_delete', models.BooleanField(default=False)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bhtapt_web.room')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='booking',
            name='reservation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservation_booking', to='bhtapt_web.reservation'),
        ),
    ]
