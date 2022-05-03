import pytest
from daycare.models import DayCare, Image


@pytest.fixture
def create_daycare_user():
    return DayCare.create(email="test@gmail.com", username="testuser01", password="pass",
                          name="Puppies", description="This is the first daycare test",
                          price_per_day=10,
                          capacity=50, area="Merkaz", city="Tel-Aviv", address="The best street 5")


@pytest.fixture
def create_image1(create_daycare_user):
    return Image.create(url="../../static/images/daycare_image_test_01.jpeg", daycare_id=create_daycare_user)


@pytest.fixture
def create_image2(create_daycare_user):
    return Image.create(url="../../static/images/daycare_image_test_02.jpeg", daycare_id=create_daycare_user)
