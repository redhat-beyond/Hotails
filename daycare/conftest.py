import pytest
from .models import DayCare, Image

EMAIL = "test@gmail.com"
USERNAME = "testuser01"
PASSWORD = "pass"
NAME = "Puppies"
DESCRIPTION = "This is the first daycare test"
PRICE_PER_DAY = 10
CAPACITY = 50
AREA = "Merkaz"
CITY = "Tel-Aviv"
ADDRESS = "The best street 5"
TEST_IMAGE_URL_01 = "../../static/images/daycare_image_test_01.jpeg"
TEST_IMAGE_URL_02 = "../../static/images/daycare_image_test_02.jpeg"


@pytest.fixture
def create_daycare_user():
    return DayCare.create(email=EMAIL, username=USERNAME, password=PASSWORD,
                          name=NAME, description=DESCRIPTION,
                          price_per_day=PRICE_PER_DAY,
                          capacity=CAPACITY, area=AREA, city=CITY, address=ADDRESS)


@pytest.fixture
def create_image1(create_daycare_user):
    return Image.create(url=TEST_IMAGE_URL_01, daycare_id=create_daycare_user)


@pytest.fixture
def create_image2(create_daycare_user):
    return Image.create(url=TEST_IMAGE_URL_02, daycare_id=create_daycare_user)
