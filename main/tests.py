import pytest
from dogowner.models import DogOwner
from daycare.models import DayCare
from orders.models import Order


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

    def test_valid_login_daycare_user_info(self, client, create_daycare_user, daycare_data):
        previous_logged_user = client.get('/').wsgi_request.user
        form = {'username': pytest.DAYCARE_USERNAME,
                'password': pytest.DAYCARE_PASSWORD,
                }

        response = client.post('/login/', form, follow=True)
        current_log_user = response.wsgi_request.user
        assert current_log_user == create_daycare_user.user
        assert previous_logged_user != current_log_user

    def test_invalid_login_daycare_user_info(self, client):
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

    def test_root_entrypoint_redirection_logged_daycare_user(self, client, create_daycare_user):
        client.force_login(user=create_daycare_user.user)
        response = client.get("/")
        assert response.status_code == 302
        assert response['Location'] == '/homepage/'


@pytest.mark.django_db
class TestHomepageView:
    def test_unlogged_user_access_to_homepage(self, client):
        response = client.get("/homepage/")
        assert response.status_code == 302
        assert response['Location'] == '/login/?next=/homepage/'


@pytest.mark.django_db
class TestDogOwnerHomePageView:
    def test_dog_owner_homepage_present_all_daycares(self, client, create_dog_owner_user):
        client.force_login(user=create_dog_owner_user.user)
        response = client.get("/homepage/")
        assert response.status_code == 200
        assert set(response.context['day_care_queryset']) == set(DayCare.objects.all())

    def test_daycare_not_appears_in_search_after_reduce_capacity_on_dates_to_0(self, client,
                                                                               create_dog_owner_user,
                                                                               create_daycare_user):
        search_form = {'area': "",
                       'city': "",
                       'price_per_day': 100,
                       'name': "",
                       'start_date': "2022-05-03",
                       'end_date': "2022-05-08",
                       }
        daycare_user = create_daycare_user
        client.force_login(user=create_dog_owner_user.user)
        response = client.post('/homepage/', search_form, follow=True)
        day_care_queryset = response.context['day_care_queryset']
        assert daycare_user in day_care_queryset

        for _ in range(daycare_user.capacity):
            Order.create(dog_owner_id=DogOwner.objects.get(id=1), daycare_id=daycare_user,
                         start_date="2022-05-02", end_date="2022-08-02", price_per_day=100).approve_order()
        response = client.post('/homepage/', search_form, follow=True)
        assert daycare_user not in response.context['day_care_queryset']

    def test_successful_dog_owner_search_for_day_care(self, client, create_dog_owner_user):
        client.force_login(user=create_dog_owner_user.user)
        search_form = {'area': "C",
                       'city': "tel aviv",
                       'price_per_day': 800,
                       'name': "",
                       'start_date': "2022-05-03",
                       'end_date': "2022-05-08",
                       }
        response = client.post('/homepage/', search_form, follow=True)
        day_care_queryset = response.context['day_care_queryset']
        available_day_cares = Order.get_all_day_cares_available_on_dates("2022-05-03", "2022-05-08")
        filter_day_cares = DayCare.objects.filter(area__startswith='C',
                                                  city__icontains="tel aviv",
                                                  price_per_day__lte=800)
        expected_queryset = available_day_cares.intersection(filter_day_cares)
        assert set(day_care_queryset) == set(expected_queryset)

    def test_search_for_day_care_with_start_date_greater_than_end_date_show_error_and_present_all_daycares(
            self, client, create_dog_owner_user):
        client.force_login(user=create_dog_owner_user.user)
        search_form = {'area': "C",
                       'city': "tel aviv",
                       'price_per_day': 800,
                       'name': "",
                       'start_date': "2022-05-03",
                       'end_date': "2022-05-01",
                       }
        response = client.post('/homepage/', search_form, follow=True)
        day_care_queryset = response.context['day_care_queryset']
        assert set(day_care_queryset) == set(DayCare.objects.all())
        assert response.context['form']._errors['end_date']
