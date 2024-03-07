# Generated by Django 4.1.5 on 2024-03-04 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bhtapt_web', '0033_alter_room_room_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile', models.CharField(max_length=20, null=True)),
                ('address', models.CharField(max_length=300, null=True)),
                ('country', models.CharField(blank=True, max_length=200, null=True)),
                ('id_proof', models.CharField(blank=True, choices=[('1', 'Driving Licence'), ('2', 'Passport'), ('3', 'PAN Card')], max_length=10, null=True)),
                ('id_no', models.CharField(blank=True, max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('soft_delete', models.BooleanField(default=False)),
            ],
        ),
    ]
