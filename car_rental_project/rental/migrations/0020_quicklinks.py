# Generated by Django 4.2.7 on 2023-12-07 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0019_delete_pickuplocation'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuickLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField()),
            ],
        ),
    ]
