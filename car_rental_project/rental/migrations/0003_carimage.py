# Generated by Django 4.2.7 on 2023-12-02 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0002_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='cars/')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='images', to='rental.car')),
            ],
        ),
    ]
