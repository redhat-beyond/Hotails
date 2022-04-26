import pytest
from .models import DayCare
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Image
import random
from review.models import Review


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

    @pytest.mark.parametrize(
        ['email', 'name', 'price_per_day',
         'area', 'city', 'address', 'expected_error_message'],
        [
            pytest.param('invalid mail format', 'test_name', 10, 'Merkaz', 'tel-aviv', 'test address',
                         "'Enter a valid email address.'", id='testing invalid email format'),
            pytest.param('test@gmail.com', 'this is very long name above 20 letters', 10, 'Merkaz', 'tel-aviv',
                         'test address', 'Invalid name - max length is 20', id='testing invalid name length'),
            pytest.param('test@gmail.com', 'test_name', 'invalid price', 'Merkaz', 'tel-aviv', 'test address',
                         'Invalid price_per_day - price should be number.', id='testing invalid price_per_day type'),
            pytest.param('test@gmail.com', 'test_name', 10000, 'Merkaz', 'tel-aviv', 'test address',
                         'Invalid price - max price is 4 digits.', id='testing invalid price_per_day length'),
            pytest.param('test@gmail.com', 'test_name', 10, 'this is very long name above 20 letters', 'tel-aviv',
                         'test address', 'Invalid area - max length is 20', id='testing invalid area length'),
            pytest.param('test@gmail.com', 'test_name', 10, 'Merkaz', 'this is very long name above 20 letters',
                         'test address', 'Invalid city - max length is 20', id='testing invalid city length'),
            pytest.param('test@gmail.com', 'test_name', 10, 'Merkaz', 'tel-aviv',
                         'this is very long name above 50 letters and maybe moreeeeeee',
                         'Invalid address - max length is 50', id='testing invalid address length')
        ],
    )
    def test_daycare_invalidations_field(self, email, name, price_per_day, area, city, address,
                                         expected_error_message):
        with pytest.raises(ValidationError, match=expected_error_message):
            DayCare.create(username='testuser02', email=email, password='test_password', name=name,
                           description='test description', price_per_day=price_per_day, capacity=50,
                           area=area, city=city, address=address)

    def test_daycare_user_creation_with_same_user_name(self, create_daycare_user):
        assert create_daycare_user.user in User.objects.all()
        assert create_daycare_user in DayCare.objects.all()

        with pytest.raises(ValidationError, match="Invalid username"):
            DayCare.create(username='testUser01', email="valid@gmail.com", password='pass123', name='daycare',
                           description='new description', price_per_day=10, capacity=50,
                           area='north', city='haifa', address='new address')

    def test_daycare_redirected_homepage_after_login(self, client, create_daycare_user):
        client.force_login(user=create_daycare_user.user)
        response = client.get('/')
        assert response.status_code == 302
        assert response['Location'] == '/homepage/'

    def test_relevant_daycare_homepage_with_static_data(self, client, create_daycare_user):
        dayCare = random.choice([daycare for daycare in DayCare.objects.all() if 'static' in daycare.user.username])
        client.force_login(user=dayCare.user)

        response = client.get('/homepage/')

        daycare_shown_in_homepage = response.context['daycare']
        assert daycare_shown_in_homepage == dayCare

        images_shown_in_homepage = set(response.context['images'])
        daycare_images = set(Image.get_images_by_daycare_id(daycare_id=dayCare.id))
        assert images_shown_in_homepage == daycare_images

        reviews_shown_in_homepage = set(response.context['reviews'])
        daycare_reviews = set(Review.get_review_by_daycare_id(daycare_id=dayCare.id))
        assert reviews_shown_in_homepage == daycare_reviews
