from django.db import migrations, transaction
import random
import textwrap

REVIEW_AND_RATE_LIST = [
    (textwrap.dedent("""The dog supervisors are awesome people and love working with dogs. Everyone I have met there is
    so friendly and warm. My dog LOVES them and is so happy to go there each morning and I am happy that we have a
    place where he can be cared for during the day when I am gone with people that he cares about and who care for
    him!"""), 5),
    (textwrap.dedent("""We left our small dog Neo at Manoir Kanisha for a weekend and could not be more impressed with
    the treatment he received. Every imaginably detail is anticipated and attended by Nicole and her caring staff.
    The facilities are of luxury hotel calibre, and every effort is made to make your pet’s stay a pleasant and calm
    one. Nicole even took some photos of Neo with my 6-year old daughter so that i could show my dad, Neo’s actual
    owner. We’re impressed beyond words, and enthusiastically recommend Kanisha to others. Thanks so much!"""), 4),
    (textwrap.dedent("""We brought our dog to Manoir Kanisha when it first opened in 1990. I was worried about him
    while on vacation so I called Nicole. She reassured me that he was doing very well and she was enhancing his meals
    with burger and rice! Kanisha is not just a place to board your dog, it’s a five star doggy hotel. Nicole and her
    staff are so very knowledgeable – and kind, caring and loving that, since 1990, I haven’t even thought about taking
    my dogs anywhere else. Sadly, this past week was the last time my little “dare devil” MAGGIE will be vacationing at
    Kanisha as we have found a new home in Nova Scotia with 2 acres of running room for her. She will miss her family
    there, as will we but when we come back for visits we’ll be dropping by to say hello. Thank you Nicole and team for
    all that you do. You have"""), 2),
    (textwrap.dedent("""I love how Laura pays attention to detail.  She wanted to make sure that she knew my little guy:
    from his treats and his routine down to the way he likes to play ball. I never worried a minute while I was out of
    town because she had everything under control. It was such a comfort knowing that my little guy didn’t have to go
    stay somewhere else, but could stay in his own routine at home.  I would HIGHLY recommend Laura and her pet sitting
    services to ALL my friends with furry people. Don’t even worry about stressing or planning for a trip to the kennel,
     just let Laura come over and take care of your little family at home. AND, she will update you as often as you’d
     like regarding your pets and their behavior.  Call her today!!"""), 3)
]


class Migration(migrations.Migration):
    dependencies = [
        ('review', '0002_test_data'),
        ('daycare', '0004_static_daycare_users'),
        ('dogowner', '0004_test_static_data'),
    ]

    def generate_data(apps, schema_editor):
        from daycare.models import DayCare
        from dogowner.models import DogOwner
        from review.models import Review

        static_daycares = [daycare for daycare in DayCare.objects.all() if 'static' in daycare.user.username]
        static_reviews = [(random.choice(REVIEW_AND_RATE_LIST), daycare.id, dogowner.id) for daycare in static_daycares
                          for dogowner in DogOwner.objects.all()]

        with transaction.atomic():
            for (review, rating), day_care_id, dog_owner_id in static_reviews:
                Review.create(review=review, rating=rating, daycare_id=day_care_id, dogowner_id=dog_owner_id)

    operations = [
        migrations.RunPython(generate_data),
    ]
