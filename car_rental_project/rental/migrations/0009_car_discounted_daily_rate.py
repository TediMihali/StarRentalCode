# Generated by Django 4.2.7 on 2023-12-04 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0008_car_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='discounted_daily_rate',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
