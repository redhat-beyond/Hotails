from django.db import migrations, transaction
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
        ('daycare', '0002_test_data'),
        ('dogowner', '0002_test_data'),
    ]

    def generate_data(apps, schema_editor):
        from daycare.models import DayCare
        from dogowner.models import DogOwner
        from orders.models import Order

        test_data = [
            ('1', '1', timezone.datetime(2022, 3, 23), timezone.datetime(2022, 3, 25), '100'),
            ('1', '2', timezone.datetime(2022, 3, 25), timezone.datetime(2022, 3, 27), '200'),
            ('2', '1', timezone.datetime(2022, 3, 28), timezone.datetime(2022, 3, 31), '500'),
            ('2', '2', timezone.datetime(2022, 3, 20), timezone.datetime(2022, 3, 21), '150'),
        ]

        with transaction.atomic():
            for dog_owner_id, daycare_id, starting_date, end_date, price_per_day in test_data:
                Order(dog_owner_id=DogOwner.objects.get(pk=dog_owner_id),
                      daycare_id=DayCare.objects.get(pk=daycare_id),
                      start_date=starting_date,
                      end_date=end_date,
                      price_per_day=price_per_day).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
