import pytest
from dogowner.models import DogOwner


@pytest.fixture
def create_dog_owner_user():
    return DogOwner.create(email='dogowner@address.com',
                           username='dogOwnerUser01',
                           password='password123',
                           dog_name='dog name',
                           first_name='test',
                           last_name='user',
                           phone_number=1234567890,
                           dog_race='dog race',
                           dog_picture_url='https://www.google.com/user1.jpg',
                           dog_age=4,
                           dog_weight=2,
                           dog_gender='M'
                           )


@pytest.mark.django_db
class TestAboutView:
    def test_redirected_to_about_section(self, client):
        response = client.get('/about')
        assert response.status_code == 301
        response = client.get(response.url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestLoginView:
    def test_enter_login_page(self, client):
        response = client.get('/login/')
        assert response.status_code == 200

    def test_valid_login_dog_owner_user_info(self, client, create_dog_owner_user):
        previous_logged_user = client.get('/').wsgi_request.user
        form = {'username': 'dogOwnerUser01',
                'password': 'password123',
                }

        response = client.post('/login/', form, follow=True)
        current_log_user = response.wsgi_request.user
        assert current_log_user == create_dog_owner_user.user
        assert previous_logged_user != current_log_user

    def test_invalid_login_dog_owner_user_info(self, client):
        form = {'username': "daycare@address.com",
                'password': "incorrect",
                }
        response = client.post('/login/', form, follow=True)
        assert response.wsgi_request.user.is_anonymous

    def test_block_logged_user_from_login_page(self, client, create_dog_owner_user):
        client.force_login(user=create_dog_owner_user.user)
        response = client.get("/login/")
        assert response['Location'] == '/'


@pytest.mark.django_db
class TestLogoutView:
    def test_successful_logout(self, client, create_dog_owner_user):
        client.force_login(user=create_dog_owner_user.user)
        logged_user = client.get('/').wsgi_request.user
        response = client.get('/logout/')
        assert response['Location'] == '/login/'
        assert response.wsgi_request.user != logged_user


@pytest.mark.django_db
class TestIndexView:
    def test_root_entrypoint_redirection_unlogged_user(self, client):
        response = client.get("/")
        assert response.status_code == 302
        assert response['Location'] == '/login/'

    def test_root_entrypoint_redirection_logged_user(self, client, create_dog_owner_user):
        client.force_login(user=create_dog_owner_user.user)
        response = client.get("/")
        assert response.status_code == 302
        assert response['Location'] == '/homepage/'


class TestHomepageView:
    def test_unlogged_user_access_to_homepage(self, client):
        response = client.get("/homepage/")
        assert response.status_code == 302
        assert response['Location'] == '/login/?next=/homepage/'
