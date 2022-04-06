from conftest import DOG_OWNER_FIXTURE_PROFILE_PICTURE_URL
from .models import DogOwner, DOG_OWNER_DEFAULT_PROFILE_PICTURE_URL
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .validators import MaxLength
import pytest


@pytest.mark.django_db
class TestDogOwnerModel:

    def test_create_dog_owner(self, create_dog_owner_user):
        assert create_dog_owner_user.user in User.objects.all()
        assert create_dog_owner_user in DogOwner.objects.all()

    def test_del_dogowner(self, create_dog_owner_user):
        dogOwner_01 = DogOwner.objects.get(first_name='NEW')
        dogOwner_01.user.delete()
        assert dogOwner_01 not in DogOwner.objects.all()
        assert dogOwner_01.user not in User.objects.all()

    def test_duplicate_creation_dog_owner_user(self):
        with pytest.raises(ValidationError, match="Invalid username - username already exist"):
            for i in range(2):
                DogOwner.create(email='testuser@gmail.com', username='SAME_USER_NAME_03', password='testpassowrd',
                                dog_name='kliford', first_name='NEW', last_name='USER',
                                phone_number=1234567890, dog_race='lavrador',
                                dog_picture_url="https://www.akc.org/wp-content/uploads/2019/06"
                                                "/Bohemian-Shepherd.1.jpg",
                                dog_age=10, dog_weight=6, dog_gender='M'
                                )

    def test_dog_owner_user_creation_with_invalid_email(self):
        with pytest.raises(ValidationError, match="'Enter a valid email address.'", ):
            DogOwner.create(email='INVALID_EMAIL', username='testuser04', password='testpassowrd',
                            dog_name='kliford', first_name='NEW', last_name='USER',
                            phone_number=1234567890, dog_race='lavrador',
                            dog_picture_url="https://www.akc.org/wp-content/uploads/2019/06/Bohemian-Shepherd.1.jpg",
                            dog_age=10, dog_weight=6, dog_gender='M'
                            )

    def test_dog_owner_user_creation_with_invalid_phone_as_txt(self):
        with pytest.raises(ValidationError, match="Invalid phone - phone should be number."):
            DogOwner.create(email='testuser@gmail.com', username='testuser05', password='testpassowrd',
                            dog_name='kliford', first_name='NEW', last_name='USER',
                            phone_number='tests', dog_race='lavrador',
                            dog_picture_url="https://www.akc.org/wp-content/uploads/2019/06/Bohemian-Shepherd.1.jpg",
                            dog_age=10, dog_weight=6, dog_gender='M'
                            )

    def test_dog_owner_user_creation_with_invalid_phone_short(self):
        with pytest.raises(ValidationError, match="Invalid phone - phone should be 10 digits."):
            DogOwner.create(email='testuser@gmail.com', username='testuser06', password='testpassowrd',
                            dog_name='kliford', first_name='NEW', last_name='USER',
                            phone_number=123456789, dog_race='lavrador',
                            dog_picture_url="https://www.akc.org/wp-content/uploads/2019/06/Bohemian-Shepherd.1.jpg",
                            dog_age=10, dog_weight=6, dog_gender='M'
                            )

    def test_dog_owner_user_creation_with_invalid_phone_long(self):
        with pytest.raises(ValidationError, match="Invalid phone - phone should be 10 digits."):
            DogOwner.create(email='testuser@gmail.com', username='testuser06', password='testpassowrd',
                            dog_name='kliford', first_name='NEW', last_name='USER',
                            phone_number=123456789123, dog_race='lavrador',
                            dog_picture_url="https://www.akc.org/wp-content/uploads/2019/06/Bohemian-Shepherd.1.jpg",
                            dog_age=10, dog_weight=6, dog_gender='M'
                            )

    def test_dog_owner_user_creation_with_invalid_dog_gender(self):
        with pytest.raises(ValidationError, match="Invalid gender - please choose 'M','F' or 'UN."):
            DogOwner.create(email='testuser@gmail.com', username='testuser07', password='testpassowrd',
                            dog_name='kliford', first_name='NEW', last_name='USER',
                            phone_number=1234567890, dog_race='lavrador',
                            dog_picture_url="https://www.akc.org/wp-content/uploads/2019/06/Bohemian-Shepherd.1.jpg",
                            dog_age=10, dog_weight=6, dog_gender='NOT_FROM_CHOICES'
                            )

    def test_dog_owner_user_creation_with_long_first_name(self):
        with pytest.raises(ValidationError,
                           match=f"""Invalid FIRST_NAME - max length is {MaxLength["FIRST_NAME"].value}."""):
            DogOwner.create(email='testuser@gmail.com', username='testuser08', password='testpassowrd',
                            dog_name='kliford', first_name='THIS FIRST NAME IS TOO LONG', last_name='USER',
                            phone_number=1234567890, dog_race='lavrador',
                            dog_picture_url="https://www.akc.org/wp-content/uploads/2019/06/Bohemian-Shepherd.1.jpg",
                            dog_age=10, dog_weight=6, dog_gender='M'
                            )

    def test_dog_owner_user_creation_with_long_last_name(self):
        with pytest.raises(ValidationError,
                           match=f"""Invalid LAST_NAME - max length is {MaxLength["LAST_NAME"].value}."""):
            DogOwner.create(email='testuser@gmail.com', username='testuser09', password='testpassowrd',
                            dog_name='kliford', first_name='NEW', last_name='THIS LAST NAME IS TOO LONG',
                            phone_number=1234567890, dog_race='lavrador',
                            dog_picture_url="https://www.akc.org/wp-content/uploads/2019/06/Bohemian-Shepherd.1.jpg",
                            dog_age=10, dog_weight=6, dog_gender='M'
                            )

    def test_dog_owner_user_creation_with_long_dog_race(self):
        with pytest.raises(ValidationError,
                           match=f"""Invalid DOG_RACE - max length is {MaxLength["DOG_RACE"].value}."""):
            DogOwner.create(email='testuser@gmail.com', username='testuser10', password='testpassowrd',
                            dog_name='kliford', first_name='NEW', last_name='USER',
                            phone_number=1234567890, dog_race='THIS DOG RACE IS TOO LONG WAY TOO LONG ',
                            dog_picture_url="https://www.akc.org/wp-content/uploads/2019/06/Bohemian-Shepherd.1.jpg",
                            dog_age=10, dog_weight=6, dog_gender='M'
                            )

    def test_dog_owner_user_creation_with_long_dog_name(self):
        with pytest.raises(ValidationError,
                           match=f"""Invalid DOG_NAME - max length is {MaxLength["DOG_NAME"].value}."""):
            DogOwner.create(email='testuser@gmail.com', username='testuser11', password='testpassowrd',
                            dog_name='THIS DOG NAME IS TOO LONG', first_name='NEW', last_name='USER',
                            phone_number=1234567890, dog_race='lavrador',
                            dog_picture_url="https://www.akc.org/wp-content/uploads/2019/06/Bohemian-Shepherd.1.jpg",
                            dog_age=10, dog_weight=6, dog_gender='M'
                            )

    def test_dog_owner_user_creation_with_non_alfa_first_name(self):
        with pytest.raises(ValidationError, match="Invalid FIRST_NAME -"
                                                  " please enter only alphabet and space characters."):
            DogOwner.create(email='testuser@gmail.com', username='testuser12', password='testpassowrd',
                            dog_name='kliford', first_name='FIRSTNAME1', last_name='USER',
                            phone_number=1234567890, dog_race='lavrador',
                            dog_picture_url="https://www.akc.org/wp-content/uploads/2019/06/Bohemian-Shepherd.1.jpg",
                            dog_age=10, dog_weight=6, dog_gender='M'
                            )

    def test_dog_owner_user_creation_with_non_alfa_last_name(self):
        with pytest.raises(ValidationError, match="Invalid LAST_NAME -"
                                                  " please enter only alphabet and space characters."):
            DogOwner.create(email='testuser@gmail.com', username='testuser13', password='testpassowrd',
                            dog_name='kliford', first_name='NEW', last_name='LASTNAME2',
                            phone_number=1234567890, dog_race='lavrador',
                            dog_picture_url="https://www.akc.org/wp-content/uploads/2019/06/Bohemian-Shepherd.1.jpg",
                            dog_age=10, dog_weight=6, dog_gender='M'
                            )

    def test_dog_owner_user_creation_with_non_alfa_dog_race(self):
        with pytest.raises(ValidationError, match="Invalid DOG_RACE -"
                                                  " please enter only alphabet and space characters."):
            DogOwner.create(email='testuser@gmail.com', username='testuser14', password='testpassowrd',
                            dog_name='kliford', first_name='NEW', last_name='USER',
                            phone_number=1234567890, dog_race='DOGRACE1',
                            dog_picture_url="https://www.akc.org/wp-content/uploads/2019/06/Bohemian-Shepherd.1.jpg",
                            dog_age=10, dog_weight=6, dog_gender='M'
                            )

    def test_dog_owner_user_creation_with_non_alfa_dog_name(self):
        with pytest.raises(ValidationError, match="Invalid DOG_NAME -"
                                                  " please enter only alphabet and space characters."):
            DogOwner.create(email='testuser@gmail.com', username='testuser15', password='testpassowrd',
                            dog_name='DOGNAME1', first_name='NEW', last_name='USER',
                            phone_number=1234567890, dog_race='lavrador',
                            dog_picture_url="https://www.akc.org/wp-content/uploads/2019/06/Bohemian-Shepherd.1.jpg",
                            dog_age=10, dog_weight=6, dog_gender='M'
                            )

    def test_dog_owner_user_creation_with_url_not_an_image(self):
        with pytest.raises(ValidationError,
                           match="""Invalid  image URL  - URL should end with '.png', '.jpg' or '.jpeg'."""):
            DogOwner.create(email='testuser@gmail.com', username='testuser17', password='testpassowrd',
                            dog_name='kliford', first_name='NEW', last_name='USER',
                            phone_number=1234567890, dog_race='lavrador',
                            dog_picture_url="https://www.not/an/image.com",
                            dog_age=10, dog_weight=6, dog_gender='M'
                            )

    def test_dogowner_has_customized_profile_image(self, create_dog_owner_user: DogOwner):
        dogowner_profile_image = create_dog_owner_user.get_dog_owner_profile_image_url()
        assert dogowner_profile_image == DOG_OWNER_FIXTURE_PROFILE_PICTURE_URL

    def test_dogowner_has_default_profile_image(self, create_dog_owner_user: DogOwner):
        create_dog_owner_user.dog_picture_url = None
        dogowner_profile_image = create_dog_owner_user.get_dog_owner_profile_image_url()
        assert dogowner_profile_image == DOG_OWNER_DEFAULT_PROFILE_PICTURE_URL
