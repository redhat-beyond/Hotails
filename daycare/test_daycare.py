import pytest
from .models import DayCare
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


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


@pytest.mark.django_db()
class TestDaycareModel:
    def test_persist_daycare(self, create_daycare_user):
        assert create_daycare_user.user in User.objects.all()
        assert create_daycare_user in DayCare.objects.all()

    def test_del_daycare(self, create_daycare_user):
        assert create_daycare_user.user in User.objects.all()
        assert create_daycare_user in DayCare.objects.all()

        create_daycare_user.delete()
        assert create_daycare_user not in DayCare.objects.all()
        assert create_daycare_user not in User.objects.all()

    def test_daycare_user_delete(self, create_daycare_user):
        assert create_daycare_user.user in User.objects.all()
        assert create_daycare_user in DayCare.objects.all()

        create_daycare_user.user.delete()
        assert create_daycare_user not in DayCare.objects.all()

    def test_daycare_user_creation_with_invalid_email(self):
        with pytest.raises(ValidationError, match="'Enter a valid email address.'"):
            DayCare.create(username='testuser02', email="invalid mail format", password=PASSWORD,
                           name=NAME, description=DESCRIPTION,
                           price_per_day=PRICE_PER_DAY,
                           capacity=CAPACITY, area=AREA, city=CITY, address=ADDRESS)

    def test_daycare_user_creation_with_same_user_name(self):
        with pytest.raises(ValidationError, match="Invalid username"):
            DayCare.create(email=EMAIL, username="testuser01", password=PASSWORD,
                           name=NAME, description=DESCRIPTION,
                           price_per_day=PRICE_PER_DAY,
                           capacity=CAPACITY, area=AREA, city=CITY, address=ADDRESS)
            DayCare.create(email=EMAIL, username="testuser01", password=PASSWORD,
                           name=NAME, description=DESCRIPTION,
                           price_per_day=PRICE_PER_DAY,
                           capacity=CAPACITY, area=AREA, city=CITY, address=ADDRESS)

    def test_daycare_user_with_invalid_name(self):
        with pytest.raises(ValidationError, match="Invalid name - max length is 20"):
            DayCare.create(username=USERNAME, email=EMAIL, password=PASSWORD,
                           name="this is very long name above 20 letters and maybe moreeeeeee",
                           description=DESCRIPTION,
                           price_per_day=PRICE_PER_DAY,
                           capacity=CAPACITY, area=AREA, city=CITY, address=ADDRESS)

    def test_daycare_user_with_invalid_price_per_day_as_txt(self):
        with pytest.raises(ValidationError, match="Invalid price_per_day - price should be number."):
            DayCare.create(username=USERNAME, email=EMAIL, password=PASSWORD,
                           name=NAME, description=DESCRIPTION,
                           price_per_day="test",
                           capacity=CAPACITY, area=AREA, city=CITY, address=ADDRESS)

    def test_daycare_user_with_invalid_price_per_day_long(self):
        with pytest.raises(ValidationError, match="Invalid price - max price is 4 digits."):
            DayCare.create(username=USERNAME, email=EMAIL, password=PASSWORD,
                           name=NAME,
                           description=DESCRIPTION,
                           price_per_day=100000,
                           capacity=CAPACITY, area=AREA, city=CITY, address=ADDRESS)

    def test_daycare_user_with_invalid_area_length(self):
        with pytest.raises(ValidationError, match="Invalid area - max length is 20"):
            DayCare.create(username=USERNAME, email=EMAIL, password=PASSWORD,
                           name=NAME,
                           description=DESCRIPTION,
                           price_per_day=PRICE_PER_DAY,
                           capacity=CAPACITY, area="this is very long name above 20 letters and maybe "
                                                   "moreeeeeee", city=CITY, address=ADDRESS)

    def test_daycare_user_with_invalid_city_length(self):
        with pytest.raises(ValidationError, match="Invalid city - max length is 20"):
            DayCare.create(username=USERNAME, email=EMAIL, password=PASSWORD,
                           name=NAME,
                           description=DESCRIPTION,
                           price_per_day=PRICE_PER_DAY,
                           capacity=CAPACITY, area=AREA, city="this is very long name above 20 letters "
                                                              "and maybe "
                                                              "moreeeeeee", address=ADDRESS)

    def test_daycare_user_with_invalid_address_length(self):
        with pytest.raises(ValidationError, match="Invalid address - max length is 50."):
            DayCare.create(username=USERNAME, email=EMAIL, password=PASSWORD,
                           name=NAME,
                           description=DESCRIPTION,
                           price_per_day=PRICE_PER_DAY,
                           capacity=CAPACITY, area=AREA, city=CITY, address="this is very long name above 50 letters "
                                                                            "and maybe "
                                                                            "moreeeeeee")
