from .models import DogOwner
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .validators import MaxLength
import pytest

EMAIL = 'testuser@gmail.com'
USERNAME = 'testuser01'
PASSWORD = 'testpassowrd'
DOG_NAME = 'kliford'
FIRST_NAME = 'NEW'
LAST_NAME = 'USER'
PHONE_NUMBER = 1234567890
DOG_RACE = 'lavrador'
DOG_PICTURE_URL = 'https://www.google.com/'
DOG_AGE = 10
DOG_WEIGHT = 6
DOG_GENDER = 'M'


@pytest.fixture
def create_dog_owner_user():
    return DogOwner.create(email=EMAIL,
                           username=USERNAME,
                           password=PASSWORD,
                           dog_name=DOG_NAME,
                           first_name=FIRST_NAME,
                           last_name=LAST_NAME,
                           phone_number=PHONE_NUMBER,
                           dog_race=DOG_RACE,
                           dog_picture_url=DOG_PICTURE_URL,
                           dog_age=DOG_AGE,
                           dog_weight=DOG_WEIGHT,
                           dog_gender=DOG_GENDER
                           )


@pytest.mark.django_db
class TestDogOwnerModel:

    def test_create_dog_owner(self, create_dog_owner_user):
        assert create_dog_owner_user.user in User.objects.all()
        assert create_dog_owner_user in DogOwner.objects.all()

    def test_del_dogowner(self, create_dog_owner_user):
        dogOwner_01 = DogOwner.objects.get(first_name=FIRST_NAME)
        dogOwner_01.user.delete()
        assert dogOwner_01 not in DogOwner.objects.all()
        assert dogOwner_01.user not in User.objects.all()

    def test_duplicate_creation_dog_owner_user(self):
        with pytest.raises(ValidationError, match="Invalid username - username already exist"):
            for i in range(2):
                DogOwner.create(email=EMAIL, username='SAME_USER_NAME_03', password=PASSWORD,
                                dog_name=DOG_NAME, first_name=FIRST_NAME, last_name=LAST_NAME,
                                phone_number=PHONE_NUMBER, dog_race=DOG_RACE, dog_picture_url=DOG_PICTURE_URL,
                                dog_age=DOG_AGE, dog_weight=DOG_WEIGHT, dog_gender=DOG_GENDER
                                )

    def test_dog_owner_user_creation_with_invalid_email(self):
        with pytest.raises(ValidationError, match="'Enter a valid email address.'", ):
            DogOwner.create(email='INVALID_EMAIL', username='testuser02', password=PASSWORD,
                            dog_name=DOG_NAME, first_name=FIRST_NAME, last_name=LAST_NAME,
                            phone_number=PHONE_NUMBER, dog_race=DOG_RACE, dog_picture_url=DOG_PICTURE_URL,
                            dog_age=DOG_AGE, dog_weight=DOG_WEIGHT, dog_gender=DOG_GENDER
                            )

    def test_dog_owner_user_creation_with_invalid_dog_picture_url(self):
        with pytest.raises(ValidationError, match="Enter a valid URL."):
            DogOwner.create(email=EMAIL, username='testuser04', password=PASSWORD,
                            dog_name=DOG_NAME, first_name=FIRST_NAME, last_name=LAST_NAME,
                            phone_number=PHONE_NUMBER, dog_race=DOG_RACE, dog_picture_url='NOT_A_URL',
                            dog_age=DOG_AGE, dog_weight=DOG_WEIGHT, dog_gender=DOG_GENDER
                            )

    def test_dog_owner_user_creation_with_invalid_phone_as_txt(self):
        with pytest.raises(ValidationError, match="Invalid phone - phone should be number."):
            DogOwner.create(email=EMAIL, username='testuser05', password=PASSWORD,
                            dog_name=DOG_NAME, first_name=FIRST_NAME, last_name=LAST_NAME,
                            phone_number='tests', dog_race=DOG_RACE, dog_picture_url=DOG_PICTURE_URL,
                            dog_age=DOG_AGE, dog_weight=DOG_WEIGHT, dog_gender=DOG_GENDER
                            )

    def test_dog_owner_user_creation_with_invalid_phone_short(self):
        with pytest.raises(ValidationError, match="Invalid phone - phone should be 10 digits."):
            DogOwner.create(email=EMAIL, username='testuser06', password=PASSWORD,
                            dog_name=DOG_NAME, first_name=FIRST_NAME, last_name=LAST_NAME,
                            phone_number=123456789, dog_race=DOG_RACE, dog_picture_url=DOG_PICTURE_URL,
                            dog_age=DOG_AGE, dog_weight=DOG_WEIGHT, dog_gender=DOG_GENDER
                            )

    def test_dog_owner_user_creation_with_invalid_phone_long(self):
        with pytest.raises(ValidationError, match="Invalid phone - phone should be 10 digits."):
            DogOwner.create(email=EMAIL, username='testuser06', password=PASSWORD,
                            dog_name=DOG_NAME, first_name=FIRST_NAME, last_name=LAST_NAME,
                            phone_number=123456789123, dog_race=DOG_RACE, dog_picture_url=DOG_PICTURE_URL,
                            dog_age=DOG_AGE, dog_weight=DOG_WEIGHT, dog_gender=DOG_GENDER
                            )

    def test_dog_owner_user_creation_with_invalid_dog_gender(self):
        with pytest.raises(ValidationError, match="Invalid gender - please choose 'M','F' or 'UN."):
            DogOwner.create(email=EMAIL, username='testuser07', password=PASSWORD,
                            dog_name=DOG_NAME, first_name=FIRST_NAME, last_name=LAST_NAME,
                            phone_number=PHONE_NUMBER, dog_race=DOG_RACE, dog_picture_url=DOG_PICTURE_URL,
                            dog_age=DOG_AGE, dog_weight=DOG_WEIGHT, dog_gender='NOT_FROM_CHOICES'
                            )

    def test_dog_owner_user_creation_with_long_first_name(self):
        with pytest.raises(ValidationError,
                           match=f"""Invalid FIRST_NAME - max length is {MaxLength["FIRST_NAME"].value}."""):
            DogOwner.create(email=EMAIL, username='testuser08', password=PASSWORD,
                            dog_name=DOG_NAME, first_name='THIS FIRST NAME IS TOO LONG', last_name=LAST_NAME,
                            phone_number=PHONE_NUMBER, dog_race=DOG_RACE, dog_picture_url=DOG_PICTURE_URL,
                            dog_age=DOG_AGE, dog_weight=DOG_WEIGHT, dog_gender=DOG_GENDER
                            )

    def test_dog_owner_user_creation_with_long_last_name(self):
        with pytest.raises(ValidationError,
                           match=f"""Invalid LAST_NAME - max length is {MaxLength["LAST_NAME"].value}."""):
            DogOwner.create(email=EMAIL, username='testuser09', password=PASSWORD,
                            dog_name=DOG_NAME, first_name=FIRST_NAME, last_name='THIS LAST NAME IS TOO LONG',
                            phone_number=PHONE_NUMBER, dog_race=DOG_RACE, dog_picture_url=DOG_PICTURE_URL,
                            dog_age=DOG_AGE, dog_weight=DOG_WEIGHT, dog_gender=DOG_GENDER
                            )

    def test_dog_owner_user_creation_with_long_dog_race(self):
        with pytest.raises(ValidationError,
                           match=f"""Invalid DOG_RACE - max length is {MaxLength["DOG_RACE"].value}."""):
            DogOwner.create(email=EMAIL, username='testuser10', password=PASSWORD,
                            dog_name=DOG_NAME, first_name=FIRST_NAME, last_name=LAST_NAME,
                            phone_number=PHONE_NUMBER, dog_race='THIS DOG RACE IS TOO LONG WAY TOO LONG ',
                            dog_picture_url=DOG_PICTURE_URL,
                            dog_age=DOG_AGE, dog_weight=DOG_WEIGHT, dog_gender=DOG_GENDER
                            )

    def test_dog_owner_user_creation_with_long_dog_name(self):
        with pytest.raises(ValidationError,
                           match=f"""Invalid DOG_NAME - max length is {MaxLength["DOG_NAME"].value}."""):
            DogOwner.create(email=EMAIL, username='testuser11', password=PASSWORD,
                            dog_name='THIS DOG NAME IS TOO LONG', first_name=FIRST_NAME, last_name=LAST_NAME,
                            phone_number=PHONE_NUMBER, dog_race=DOG_RACE,
                            dog_picture_url=DOG_PICTURE_URL,
                            dog_age=DOG_AGE, dog_weight=DOG_WEIGHT, dog_gender=DOG_GENDER
                            )

    def test_dog_owner_user_creation_with_non_alfa_first_name(self):
        with pytest.raises(ValidationError, match="Invalid FIRST_NAME -"
                                                  " please enter only alphabet and space characters."):
            DogOwner.create(email=EMAIL, username='testuser12', password=PASSWORD,
                            dog_name=DOG_NAME, first_name='FIRSTNAME1', last_name=LAST_NAME,
                            phone_number=PHONE_NUMBER, dog_race=DOG_RACE, dog_picture_url=DOG_PICTURE_URL,
                            dog_age=DOG_AGE, dog_weight=DOG_WEIGHT, dog_gender=DOG_GENDER
                            )

    def test_dog_owner_user_creation_with_non_alfa_last_name(self):
        with pytest.raises(ValidationError, match="Invalid LAST_NAME -"
                                                  " please enter only alphabet and space characters."):
            DogOwner.create(email=EMAIL, username='testuser13', password=PASSWORD,
                            dog_name=DOG_NAME, first_name=FIRST_NAME, last_name='LASTNAME2',
                            phone_number=PHONE_NUMBER, dog_race=DOG_RACE, dog_picture_url=DOG_PICTURE_URL,
                            dog_age=DOG_AGE, dog_weight=DOG_WEIGHT, dog_gender=DOG_GENDER
                            )

    def test_dog_owner_user_creation_with_non_alfa_dog_race(self):
        with pytest.raises(ValidationError, match="Invalid DOG_RACE -"
                                                  " please enter only alphabet and space characters."):
            DogOwner.create(email=EMAIL, username='testuser14', password=PASSWORD,
                            dog_name=DOG_NAME, first_name=FIRST_NAME, last_name=LAST_NAME,
                            phone_number=PHONE_NUMBER, dog_race='DOGRACE1', dog_picture_url=DOG_PICTURE_URL,
                            dog_age=DOG_AGE, dog_weight=DOG_WEIGHT, dog_gender=DOG_GENDER
                            )

    def test_dog_owner_user_creation_with_non_alfa_dog_name(self):
        with pytest.raises(ValidationError, match="Invalid DOG_NAME -"
                                                  " please enter only alphabet and space characters."):
            DogOwner.create(email=EMAIL, username='testuser15', password=PASSWORD,
                            dog_name='DOGNAME1', first_name=FIRST_NAME, last_name=LAST_NAME,
                            phone_number=PHONE_NUMBER, dog_race=DOG_RACE, dog_picture_url=DOG_PICTURE_URL,
                            dog_age=DOG_AGE, dog_weight=DOG_WEIGHT, dog_gender=DOG_GENDER
                            )
