from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('dogowner', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from dogowner.models import DogOwner

        test_data = [
            ('user1@address.com', 'testUser1', 'password123', 'dog name', 'first name', 'last name',
             1234567890, 'dog race', 'https://www.google.com/user1.jpg', 4, 2, 'M'),
            ('user2@address.com', 'testUser2', 'password123', 'dog name', 'first name', 'last name',
             1234567890, 'dog race', 'https://www.google.com/user2.jpg', 3, 1, 'M'),
            ('user3@address.com', 'testUser3', 'password123', 'dog name', 'first name', 'last name',
             1234567890, 'dog race', 'https://www.google.com/user3.jpg', 2, 5, 'M'),
        ]

        with transaction.atomic():
            for (email, username, password, dog_name, first_name, last_name, phone_number, dog_race, dog_picture_url,
                 dog_age, dog_weight, dog_gender) in test_data:
                DogOwner.create(email=email,
                                username=username,
                                password=password,
                                dog_name=dog_name,
                                first_name=first_name,
                                last_name=last_name,
                                phone_number=phone_number,
                                dog_race=dog_race,
                                dog_picture_url=dog_picture_url,
                                dog_age=dog_age,
                                dog_weight=dog_weight,
                                dog_gender=dog_gender)

    operations = [
        migrations.RunPython(generate_data),
    ]
