import pytest
import datetime
from django.utils import timezone
from message.models import Message, AuthorOptions
from daycare.models import DayCare, Image
from dogowner.models import DogOwner
from orders.models import Order
from review.models import Review


@pytest.fixture
def create_order():
    return Order.create(dog_owner_id=DogOwner.objects.get(id=1),
                        daycare_id=DayCare.objects.get(id=1),
                        start_date=timezone.now(),
                        end_date=timezone.now() + datetime.timedelta(days=3),
                        price_per_day=100,
                        )


@pytest.fixture
def dogowner_message_to_daycare1():
    return Message.create(author=AuthorOptions.DogOwner,
                          dogowner_id=DogOwner.objects.get(pk=1),
                          daycare_id=DayCare.objects.get(pk=1),
                          text='Hello this is the test message1 from owner to day care')


@pytest.fixture
def daycare1_reply_to_dogonwer_message():
    return Message.create(author=AuthorOptions.DayCare,
                          dogowner_id=DogOwner.objects.get(pk=1),
                          daycare_id=DayCare.objects.get(pk=1),
                          text='This is reply to first message from daycare to owner')


@pytest.fixture
def daycare2_message_to_dogowner():
    return Message.create(author=AuthorOptions.DayCare,
                          dogowner_id=DogOwner.objects.get(pk=1),
                          daycare_id=DayCare.objects.get(pk=2),
                          text='Hello this new chat between daycare2 and dogowner')


@pytest.fixture
def daycare3_message_to_dogowner():
    return Message.create(author=AuthorOptions.DayCare,
                          dogowner_id=DogOwner.objects.get(pk=1),
                          daycare_id=DayCare.objects.get(pk=3),
                          text='new chat between daycare3 and dogowner')


@pytest.fixture
def create_dog_owner_user():
    return DogOwner.create(email='testuser@gmail.com',
                           username='testDogOwner',
                           password='testpassowrd',
                           dog_name='kliford',
                           first_name='NEW',
                           last_name='USER',
                           phone_number=1234567890,
                           dog_race='lavrador',
                           dog_picture_url="https://www.akc.org/wp-content/uploads/2019/06/Bohemian-Shepherd.1.jpg",
                           dog_age=10,
                           dog_weight=6,
                           dog_gender='M'
                           )


@pytest.fixture
def daycare_data():
    pytest.EMAIL = "test@gmail.com"
    pytest.DAYCARE_USERNAME = "testDayCare"
    pytest.DAYCARE_PASSWORD = "pass"
    pytest.NAME = "Puppies"
    pytest.DESCRIPTION = "This is the first daycare test"
    pytest.PRICE_PER_DAY = 10
    pytest.CAPACITY = 50
    pytest.AREA = "Merkaz"
    pytest.CITY = "Tel-Aviv"
    pytest.ADDRESS = "The best street 5"


@pytest.fixture
def create_daycare_user(daycare_data):
    return DayCare.create(email=pytest.EMAIL, username=pytest.DAYCARE_USERNAME, password=pytest.DAYCARE_PASSWORD,
                          name=pytest.NAME, description=pytest.DESCRIPTION, price_per_day=pytest.CAPACITY,
                          capacity=pytest.CAPACITY, area=pytest.AREA, city=pytest.CITY, address=pytest.ADDRESS)


@pytest.fixture
def create_image1(create_daycare_user):
    return Image.create(url="../../static/images/daycare_image_test_01.jpeg", daycare_id=create_daycare_user)


@pytest.fixture
def create_image2(create_daycare_user):
    return Image.create(url="../../static/images/daycare_image_test_02.jpeg", daycare_id=create_daycare_user)


@pytest.fixture
def review_data(create_dog_owner_user, create_daycare_user):
    pytest.REVIEW = 'sample review'
    pytest.RATING = 5
    pytest.DAY_CARE_ID = create_daycare_user.id
    pytest.DOG_OWNER_ID = create_dog_owner_user.id


@pytest.fixture
def review(review_data):
    return Review.create(review=pytest.REVIEW, rating=pytest.RATING, daycare_id=pytest.DAY_CARE_ID,
                         dogowner_id=pytest.DOG_OWNER_ID)
