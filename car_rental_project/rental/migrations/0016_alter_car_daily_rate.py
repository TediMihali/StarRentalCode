# Generated by Django 4.2.7 on 2023-12-06 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0015_booking_total_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='daily_rate',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
