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

    @pytest.mark.parametrize("dog_owner_1_id, dog_owner_2_id, delta_1, delta_2, capacity, expected_result",
                             [(1, 2, 3, 5, 1, False),
                              (2, 5, 4, 3, 10, True),
                              (5, 4, 6, 7, 15, True),
                              (4, 3, 4, 2, 1, False)])
    def test_order_is_approvable_according_to_daycare_capacity(self,
                                                               dog_owner_1_id: DogOwner,
                                                               dog_owner_2_id: DogOwner,
                                                               delta_1: int,
                                                               delta_2: int,
                                                               capacity: int,
                                                               expected_result: bool):
        daycare = DayCare.create("capacity_email@gmail.com", "CapacityUserName", "CapacityPassword", "CapacityName",
                                 "Changeable capacity", 100, capacity, "Merkaz", "Tel Aviv", "Capacity 123")
        dog_owner_1 = DogOwner.objects.get(id=dog_owner_1_id)
        dog_owner_2 = DogOwner.objects.get(id=dog_owner_2_id)

        order1 = Order.create(start_date=timezone.now(), end_date=timezone.now() + datetime.timedelta(days=delta_1),
                              daycare_id=daycare, dog_owner_id=dog_owner_1, price_per_day=100)
        order2 = Order.create(start_date=timezone.now(), end_date=timezone.now() + datetime.timedelta(days=delta_2),
                              daycare_id=daycare, dog_owner_id=dog_owner_2, price_per_day=100)

        order1.approve_order()
        assert order2.is_the_order_approvable() == expected_result

    @pytest.mark.parametrize("new_status, expected_result", [(StatusOptions.Pending, True),
                                                             (StatusOptions.Canceled, False),
                                                             (StatusOptions.Approved, True),
                                                             (StatusOptions.OnGoing, False),
                                                             (StatusOptions.Finished, False)])
    def test_order_cancellation_according_to_order_status(self,
                                                          create_order: Order,
                                                          new_status: StatusOptions,
                                                          expected_result: StatusOptions):
        create_order.status = new_status
        assert create_order.is_the_order_cancelable() == expected_result

    @pytest.mark.parametrize("new_status, expected_result", [(StatusOptions.Pending, "Pending"),
                                                             (StatusOptions.Canceled, "Canceled"),
                                                             (StatusOptions.Approved, "Approved"),
                                                             (StatusOptions.OnGoing, "Ongoing"),
                                                             (StatusOptions.Finished, "Finished")])
    def test_get_order_status_as_string(self,
                                        create_order: Order,
                                        new_status: StatusOptions,
                                        expected_result: StatusOptions):
        create_order.status = new_status
        assert create_order.get_order_status() == expected_result

    def test_get_daycare_capacity_in_dates_range(self, create_order):
        original_capacity_list = Order.get_capacity_of_daycare_in_dates_range(create_order.daycare_id,
                                                                              create_order.start_date,
                                                                              create_order.end_date)
        create_order.approve_order()
        updated_capacity_list = Order.get_capacity_of_daycare_in_dates_range(create_order.daycare_id,
                                                                             create_order.start_date,
                                                                             create_order.end_date)
        assert len(original_capacity_list) == len(updated_capacity_list)

        equality_list = [updated_capacity_list[i] == original_capacity_list[i] + 1
                         for i in range(len(original_capacity_list))]
        assert equality_list.count(True) == len(equality_list)
