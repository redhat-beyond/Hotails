from django.db import migrations, transaction

DOG_IMAGE_URL_LIST = [
    "https://www.akc.org/wp-content/uploads/2019/06/Bohemian-Shepherd.1.jpg",
    "https://www.akc.org/wp-content/uploads/2020/01/American-Bulldog-standing-in-three-quarter-view.jpg",
    "https://www.akc.org/wp-content/uploads/2017/11/German-Shepherd-Dog-running.jpg",
    "https://www.akc.org/wp-content/uploads/2017/11/Greater-Swiss-Mountain-Dog-laying-down-in-the-grass.jpg",
    "https://www.akc.org/wp-content/uploads/2017/11/Pembroke-Welsh-Corgi-standing-outdoors-in-the-fall.jpg",
    "https://static.parade.com/wp-content/uploads/2021/02/cutest-dog-breeds-golden-retriever-e1613033782856.jpg",
    "https://static.parade.com/wp-content/uploads/2021/02/cutest-dog-breeds-australian-shepard-e1613033832518.jpg",
    "https://static.parade.com/wp-content/uploads/2021/02/cutest-dog-breeds-cockapoo-e1613033932303.jpg",
    "https://static.parade.com/wp-content/uploads/2021/02/cutest-dog-breeds-shorkie-e1613033958646.jpg",
    "https://static.parade.com/wp-content/uploads/2021/02/cutest-dog-breeds-havanese-e1613033974219.jpg",
    "https://static.parade.com/wp-content/uploads/2020/12/"
    "medium-sized-dog-breeds-labrador-retriever-e1607905300608.jpg",
    "https://static.parade.com/wp-content/uploads/2021/02/cutest-dog-breeds-shiba-inu-e1613033812725.jpg",
    "https://static.parade.com/wp-content/uploads/2021/02/cutest-dog-breeds-pomsky.jpg",
    "https://static.parade.com/wp-content/uploads/2021/02/cutest-dog-breeds-bichon-frise-e1613033839797.jpg",
    "https://static.parade.com/wp-content/uploads/2021/02/cutest-dog-breeds-american-eskimo-e1613033856106.jpg",
    "https://static.parade.com/wp-content/uploads/2021/02/cutest-dog-breeds-papillon.jpg",
    "https://www.dogbreedslist.info/uploads/dog-pictures/labrador-retriever-2-2.jpg",
    "https://www.dogbreedslist.info/uploads/dog-pictures/golden-retriever-2.jpg",
    "https://www.dogbreedslist.info/uploads/dog-pictures/beagle-2.jpg",
    "https://www.dogbreedslist.info/uploads/dog-pictures/cavalier-king-charles-spaniel-2.jpg"
]


class Migration(migrations.Migration):
    dependencies = [
        ('dogowner', '0003_alter_dogowner_dog_picture_url'),
    ]

    def generate_data(apps, schema_editor):
        from dogowner.models import DogOwner

        static_dog_owners = [
            ('david00@address.com', 'David0', 'password123', "Max", 'David', 'Chen',
             4543837361, "Bohemian Shepherd", DOG_IMAGE_URL_LIST[0], 4, 10.3, 'M'),
            ('alex01@address.com', 'Alex1', 'password123', "Cooper", 'Alex', 'Johnson',
             9866708395, "American Bulldog", DOG_IMAGE_URL_LIST[1], 3, 15.2, 'F'),
            ('maria02@address.com', 'Maria2', 'password123', "Charlie", 'Maria', 'Williams',
             7889543084,  "German Shepherd", DOG_IMAGE_URL_LIST[2], 2, 12.6, 'M'),
            ('anna03@address.com', 'Anna3', 'password123', "Teddy", 'Anna', 'Brown',
             8970240485, "Greater Swiss Mountain Dog", DOG_IMAGE_URL_LIST[3], 4, 13.4, 'F'),
            ('marco04@address.com', 'Marco4', 'password123', "Bear", 'Marco', 'Jones',
             5027914306, "Pembroke Welsh Corgi", DOG_IMAGE_URL_LIST[4], 3, 11.7, 'M'),
            ('antonio05@address.com', 'Antonio', 'password123', "Milo", 'Antonio', 'Garcia',
             7978576075, "Golden Retriever", DOG_IMAGE_URL_LIST[5], 2, 10.3, 'F'),
            ('daniel06@address.com', 'Daniel', 'password123', "Bentley", 'Daniel', 'Miller',
             9501530128, "Australian Shepherd", DOG_IMAGE_URL_LIST[6], 4, 12.4, 'M'),
            ('laura07@address.com', 'Laura', 'password123', "Ollie", 'Laura', 'Davis',
             7348051295, "Cockapoo", DOG_IMAGE_URL_LIST[7], 3, 11.4, 'F'),
            ('jose08@address.com', 'Jose', 'password123', "Buddy", 'Jose', 'Rodriguez',
             2305247264, "Shorkie", DOG_IMAGE_URL_LIST[8], 2, 11.7, 'M'),
            ('sandra09@address.com', 'Sandra', 'password123', "Rocky", 'Sandra', 'Martinez',
             1372697623, "Havanese", DOG_IMAGE_URL_LIST[9], 4, 12.9, 'F'),
            ('sara10@address.com', 'Sara', 'password123', "Leo", 'Sara', 'Taylor',
             6570894063, "Labrador Retriever", DOG_IMAGE_URL_LIST[10], 3, 9.5, 'M'),
            ('carlos11@address.com', 'Carlos', 'password123', "Zeus", 'Carlos', 'White',
             1228907345, "Shiba Inu", DOG_IMAGE_URL_LIST[11], 2, 14.5, 'F'),
            ('ana12@address.com', 'Ana', 'password123', "Toby", 'Ana', 'Harris',
             9751508102, "Pomsky", DOG_IMAGE_URL_LIST[12], 4, 15.2, 'M'),
            ('michael13@address.com', 'Michael', 'password123', "Ace", 'Michael', 'Ramirez',
             3464456341, "Bichon Frise", DOG_IMAGE_URL_LIST[13], 3, 13.2, 'F'),
            ('marie14@address.com', 'Marie', 'password123', "Blue", 'Marie', 'Walker',
             1030010154, "American Eskimo", DOG_IMAGE_URL_LIST[14], 2, 12.8, 'M'),
            ('franscesco15@address.com', 'Francesco', 'password123', "Atlas", 'Francesco', 'Robinson',
             7366224214, "Papillon", DOG_IMAGE_URL_LIST[15], 3, 13.4, 'F'),
            ('martin16@address.com', 'Martin', 'password123', "Theo", 'Martin', 'Lee',
             2313898126, "Labrador Retriever", DOG_IMAGE_URL_LIST[16], 2, 15.6, 'F'),
            ('robert17@address.com', 'Robert', 'password123', "Bruno", 'Robert', 'Thompson',
             7634066063, "Golden Retriever", DOG_IMAGE_URL_LIST[17], 3, 12.7, 'M'),
            ('luis18@address.com', 'Luis', 'password123', "Louie", 'Luis', 'Sanchez',
             9029364381, "Beagle", DOG_IMAGE_URL_LIST[18], 2, 11.5, 'F'),
            ('tony19@address.com', 'Tony', 'password123', "Koda", 'Tony', 'Clark',
             5190084341, "Cavalier King Charles Spaniel", DOG_IMAGE_URL_LIST[19], 2, 10.6, 'M'),
        ]

        with transaction.atomic():
            for (email, username, password, dog_name, first_name, last_name, phone_number, dog_race, dog_picture_url,
                 dog_age, dog_weight, dog_gender) in static_dog_owners:
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
