import pytest
from .models import Review, DayCare, DogOwner
from django.core.validators import ValidationError

REVIEW = 'sample review'
RATING = 5
DAY_CARE_ID = 1
DOG_OWNER_ID = 1


@pytest.mark.django_db
@pytest.fixture
def test_review():
    return Review.create(review=REVIEW, rating=RATING, daycare_id=DAY_CARE_ID, dogowner_id=DOG_OWNER_ID)


@pytest.mark.django_db
class TestReviewModel:
    def test_persist_review(self, test_review):
        assert test_review.review == REVIEW
        assert test_review in Review.objects.all()

    def test_del_review(self, test_review):
        test_review.delete()
        assert test_review not in Review.objects.all()

    def test_rating_limit_min(self):
        with pytest.raises(ValidationError):
            Review.create(review=REVIEW, rating=-1, daycare_id=DAY_CARE_ID, dogowner_id=DOG_OWNER_ID)

    def test_rating_limit_max(self):
        with pytest.raises(ValidationError):
            Review.create(review=REVIEW, rating=6, daycare_id=DAY_CARE_ID, dogowner_id=DOG_OWNER_ID)

    def test_delete_related_daycare(self, test_review):
        daycare = DayCare.objects.get(pk=DAY_CARE_ID)

        assert daycare in DayCare.objects.all()
        assert test_review in Review.objects.all()

        daycare.delete()
        assert daycare not in DayCare.objects.all()
        assert test_review not in Review.objects.all()

    def test_delete_related_dogowner(self, test_review):
        dogowner = DogOwner.objects.get(id=DOG_OWNER_ID)

        assert dogowner in DogOwner.objects.all()
        assert test_review in Review.objects.all()

        dogowner.delete()
        assert dogowner not in DogOwner.objects.all()
        assert test_review in Review.objects.all()
