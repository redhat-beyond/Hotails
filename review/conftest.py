import pytest
from daycare.models import DayCare
from dogowner.models import DogOwner
from review.models import Review


@pytest.fixture
def daycare():
    return DayCare.create(email="daycare_review@gmail.com", username="daycare_review", password="pass",
                          name="reviewDayCare", description="This is test daycare for review", price_per_day=10,
                          capacity=50, area="Merkaz", city="Tel-Aviv", address="The best review")


@pytest.fixture
def dogowner():
    return DogOwner.create(email="dogowner_review@gmail.com", username='dogowner_review', password='pass',
                           dog_name='dogReview', first_name='firstNameReview', last_name='lastNameReview',
                           phone_number=1234567890, dog_race='review',
                           dog_picture_url='https://www.google.com/review.jpg', dog_age=1, dog_weight=1, dog_gender='M')


@pytest.fixture
def review_data():
    pytest.REVIEW = 'sample review'
    pytest.RATING = 5
    pytest.DAY_CARE_ID = 1
    pytest.DOG_OWNER_ID = 1


@pytest.fixture
def review(review_data):
    return Review.create(review=pytest.REVIEW, rating=pytest.RATING, daycare_id=pytest.DAY_CARE_ID,
                         dogowner_id=pytest.DOG_OWNER_ID)
