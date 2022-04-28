from django.db import migrations, transaction
import random

FIRST_CHAT = [
    "We would like to thank you personally for the kind service!",
    "Thanks, Bullwinkle was so sweet hope we will have a chance to host him again",
    "Bullwinkle will surely go wild with you again soon",
]
SECOND_CHAT = [
    "Hi, i would like to have some additional information about the food you feeding the dogs ",
    "Sure! we use only top quality organic food for our guests, we believe that a sated guest is a happy guest",
    "Thank you i'm already feeling calm"
]
THIRD_CHAT = [
    "Hello,our dog Vini is a bit special, he must eat a hot dog every 3 hours. hope you can take care of it!",
    "Dont worry we feed all our guests hot dogs every 3 hours, so you can keep calm",
    "Great! i will also bring his special german sausages"
]
CHATS = [FIRST_CHAT, SECOND_CHAT, THIRD_CHAT]


class Migration(migrations.Migration):
    dependencies = [
        ('message', '0002_test_data'),
        ('daycare', '0004_static_daycare_users'),
        ('dogowner', '0004_test_static_data'),
    ]

    def generate_data(apps, schema_editor):
        from daycare.models import DayCare
        from dogowner.models import DogOwner
        from message.models import Message

        static_daycares = [daycare for daycare in DayCare.objects.all() if 'static' in daycare.user.username]
        static_dogowner = [dogowner for dogowner in DogOwner.objects.all()]

        with transaction.atomic():
            for dogowner in static_dogowner:
                number_of_chats = random.randint(1, 3)
                chats_to_create = random.sample(CHATS, number_of_chats)
                daycares = random.sample(static_daycares, number_of_chats)

                for i, chat in enumerate(chats_to_create):
                    Message.create(author='O', dogowner_id=dogowner,
                                   daycare_id=daycares[i], text=chat[0])
                    Message.create(author='D', dogowner_id=dogowner,
                                   daycare_id=daycares[i], text=chat[1])
                    Message.create(author='O', dogowner_id=dogowner,
                                   daycare_id=daycares[i], text=chat[2])

    operations = [
        migrations.RunPython(generate_data),
    ]
