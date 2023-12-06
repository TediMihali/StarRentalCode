# Generated by Django 4.2.7 on 2023-12-06 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0016_alter_car_daily_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='discounted_daily_rate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
