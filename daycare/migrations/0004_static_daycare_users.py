from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('daycare', '0003_rename_image_url_image_url'),
    ]

    def generate_data(apps, schema_editor):
        from daycare.models import DayCare

        description = "Thank you for visiting, we are so excited to meet you and your pup!" \
                      " Since 2009, we have been serving the Chicago community by" \
                      " providing luxury Daycare and Boarding services for dogs." \
                      "We are open 24/7/365; We have staff on site 24 hours a day." \
                      "We offer dog daycare & play group, state of the art boarding" \
                      " accommodations, transportation, special events and various other amenities including grooming."
        password = 'password123'

        static_daycare_users = [
            ('De_Anza@gmail.com', 'staticUser01', password, 'De_Anza', description, 100, 20, 'NORTH', 'Haifa',
             'Union Street 4'),
            ('Disneyland@gmail.com', 'staticUser02', password, 'Disneyland', description, 300, 40, 'CENTER', 'Tel Aviv',
             'Fulton Street 10'),
            ('Disney_Spa@gmail.com', 'staticUser03', password, 'Disney_Spa', description, 500, 100, 'SOUTH',
                'Berrsheba', 'Summer Street 3'),
            ('Drakesbad_Guest@gmail.com', 'staticUser04', password, 'Drakesbad_Guest', description, 50, 10, 'SOUTH',
             'Ashdod', 'Andover Court 1'),
            ('Duceys_Lodge@gmail.com', 'staticUser05', password, 'Duceys_Lodge', description, 120, 35, 'CENTER',
                'Holon', 'Lexington Drive 11'),
            ('Dunbar@gmail.com', 'staticUser06', password, 'Dunbar', description, 130, 40, 'CENTER', 'Bat Yam',
             'Maple Lane 30'),
            ('East_Brother_Island@gmail.com', 'staticUser07', password, 'East_Brother_Island', description, 20, 15,
             'CENTER', 'Jaffa', 'Hawthorne Avenue 22'),
            ('El_Garces@gmail.com', 'staticUser08', password, 'El_Garces', description, 250, 70, 'NORTH', 'Nahariya',
             'Pheasant Run'),
            ('El_Carmelo@gmail.com', 'staticUser09', password, 'El_Carmelo', description, 600, 90, 'NORTH', 'Dimona',
             'Broad Street West 4'),
            ('Eureka_Inn@gmail.com', 'staticUser10', password, 'Eureka_Inn', description, 430, 40, 'CENTER', 'Tel Aviv',
             'Route 6'),
            ('Fairmont_San_Jose@gmail.com', 'staticUser11', password, 'Fairmont_San_Jose', description, 75, 45,
                'CENTER', 'Kfar Saba', 'Cedar Lane 1'),
            ('Glen_Tavern_Inn@gmail.com', 'staticUser12', password, 'Glen_Tavern_Inn', description, 350, 50, 'NORTH',
             'Nazareth', 'Fulton Street 30'),
            ('Green_Shutter@gmail.com', 'staticUser13', password, 'Green_Shutter', description, 45, 10, 'CENTER',
             'Hertzelya', 'Olive Street 3'),
            ('The_Hacienda_Milpita@gmail.com', 'staticUser14', password, 'The_Hacienda_Milpita', description, 10, 5,
             'SOUTH', 'Eilat', 'Oak Avenue 11'),
            ('Hayes_Mansion@gmail.com', 'staticUser15', password, 'Hayes_Mansion', description, 800, 70, 'NORTH',
                'Arce', 'Madison Street 14'),
            ('Hilton_Anaheim@gmail.com', 'staticUser16', password, 'Hilton_Anaheim', description, 550, 50, 'CENTER',
             'Holon', 'Fulton Street 20'),
            ('San_Diego_Bayfront@gmail.com', 'staticUser17', password, 'San_Diego_Bayfront', description, 300, 30,
             'NORTH', 'Qiryat Ata', 'Church Street 5'),
            ('Hilton_Resort@gmail.com', 'staticUser18', password, 'Hilton_Resort', description, 200, 20, 'SOUTH',
             'Ashkelon', 'Cedar Lane 40'),
            ('Holbrooke@gmail.com', 'staticUser19', password, 'Holbrooke', description, 600, 65, 'SOUTH', 'Ashdod',
             'Main Street West 22'),
            ('Hollywood_Melrose@gmail.com', 'staticUser20', password, 'Hollywood_Melrose', description, 100, 10,
             'CENTER', 'Tel Aviv', 'Elizabeth Street'),
        ]

        with transaction.atomic():
            for (email, username, password, name, description, price_per_day, capacity, area, city,
                 address) in static_daycare_users:
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
