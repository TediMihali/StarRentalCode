# Generated by Django 5.0 on 2023-12-10 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0028_alter_customer_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='phone_number',
            field=models.CharField(help_text='Please enter your phone number +2556912345678', max_length=12, null=True),
        ),
    ]
