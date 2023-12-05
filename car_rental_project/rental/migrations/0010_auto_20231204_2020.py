from django.db import migrations

def set_discounted_daily_rate(apps, schema_editor):
    Car = apps.get_model('rental', 'Car')
    for car in Car.objects.all():
        car.discounted_daily_rate = int(0.8 * car.daily_rate)
        car.save()

class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0009_car_discounted_daily_rate'),
    ]

    
    operations = [
        migrations.RunPython(set_discounted_daily_rate),
    ]