from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('daycare', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from daycare.models import DayCare

        test_data = [
            ('user1@address.com', 'testUser01', 'password123', 'daycare01', 'first description', 10,
             100, 'north', 'tel-aviv', 'street 01'),
            ('user2@address.com', 'testUser02', 'password123', 'daycare02', 'second description', 10,
             100, 'north', 'tel-aviv', 'street 02'),
            ('user3@address.com', 'testUser03', 'password123', 'daycare03', 'third description', 10,
             100, 'north', 'tel-aviv', 'street 03'),
        ]

        with transaction.atomic():
            for (email, username, password, name, description, price_per_day, capacity, area, city,
                 address) in test_data:
                DayCare.create(email=email,
                               username=username,
                               password=password,
                               name=name,
                               description=description,
                               price_per_day=price_per_day,
                               capacity=capacity,
                               area=area,
                               city=city,
                               address=address,
                               )

    operations = [
        migrations.RunPython(generate_data),
    ]
