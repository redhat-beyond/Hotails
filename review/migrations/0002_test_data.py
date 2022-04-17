from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('review', '0001_initial'),
        ('daycare', '0002_test_data'),
        ('dogowner', '0002_test_data'),
    ]

    def generate_data(apps, schema_editor):
        from review.models import Review
        test_data = [
            ('review 1', 1, 1, 1),
            ('review 2', 2, 1, 2),
            ('review 3', 3, 1, 3),
            ('review 4', 4, 2, 1),
            ('review 5', 5, 2, 2),
            ('review 5', 5, 2, 3),
        ]

        with transaction.atomic():
            for review, rating, day_care_id, dog_owner_id in test_data:
                Review.create(review=review, rating=rating, daycare_id=day_care_id, dogowner_id=dog_owner_id)

    operations = [
        migrations.RunPython(generate_data),
    ]
