import datetime
from django.utils import timezone
from dogowner.models import DogOwner
from daycare.models import DayCare
from .models import Order
from .models import StatusOptions
import pytest


@pytest.mark.django_db
class TestOrderModel:
    def test_create_order(self, create_order):
        assert create_order in Order.objects.all()

    def test_delete_order(self, create_order):
        assert create_order in Order.objects.all()
        create_order.delete()
        assert create_order not in Order.objects.all()

    def test_approve_order(self, create_order):
        create_order.approve_order()

        assert create_order.status == StatusOptions.Approved
        assert create_order.approval_date is not None

    def test_cancel_order(self, create_order):
        create_order.cancel_order()

        assert create_order.status == StatusOptions.Canceled
        assert create_order.cancellation_date is not None

    @pytest.mark.parametrize('price_per_day, num_of_days, expected_result',
                             [
                                 (100, 3, 300),
                                 (50, 6, 300),
                                 (500, 5, 2500),
                                 (7, 1, 7),
                             ])
    def test_total_price_of_order(self, price_per_day, num_of_days, expected_result):
        new_order = Order.create(dog_owner_id=DogOwner.objects.get(id=1),
                                 daycare_id=DayCare.objects.get(id=1),
                                 start_date=timezone.now(),
                                 end_date=timezone.now() + datetime.timedelta(days=num_of_days),
                                 price_per_day=price_per_day,
                                 )
        assert new_order.get_order_total_price() == expected_result

    def test_dog_owner_id_is_deleted_when_dog_owner_is_deleted(self, create_order):
        DogOwner.objects.get(id=1).delete()
        assert Order.objects.get(id=create_order.id).dog_owner_id is None

    def test_daycare_id_is_deleted_when_daycare_is_deleted(self, create_order):
        DayCare.objects.get(id=1).delete()
        assert Order.objects.get(id=create_order.id).daycare_id is None

    @pytest.mark.parametrize('start_date, end_date',
                             [
                                 ("2022-05-02", "2022-08-02"),
                             ])
    def test_day_care_available_on_dates_appears_in_available_day_cares_queryset(self, create_daycare_user,
                                                                                 start_date, end_date):
        day_care_user = create_daycare_user
        assert day_care_user in Order.get_all_day_cares_available_on_dates(start_date, end_date)

    @pytest.mark.parametrize('start_date, end_date',
                             [
                                 ("2022-05-02", "2022-08-02"),
                             ])
    def test_day_care_not_available_on_dates_not_appears_in_available_day_cares_queryset(self, create_daycare_user,
                                                                                         start_date, end_date):
        day_care_user = create_daycare_user
        for _ in range(day_care_user.capacity):
            Order.create(dog_owner_id=DogOwner.objects.get(id=1), daycare_id=day_care_user,
                         start_date=start_date, end_date=end_date, price_per_day=500).approve_order()
        assert day_care_user not in Order.get_all_day_cares_available_on_dates(start_date, end_date)
