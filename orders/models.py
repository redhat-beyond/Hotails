from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from daycare.models import DayCare
from dogowner.models import DogOwner
import datetime


class StatusOptions(models.TextChoices):
    Pending = 'P', 'Pending'
    Approved = 'A', 'Approved'
    Canceled = 'C', 'Canceled'
    Finished = 'F', 'Finished'
    OnGoing = 'O', 'On Going'


class Order(models.Model):
    dog_owner_id = models.ForeignKey(DogOwner, null=True, on_delete=models.SET_NULL)
    daycare_id = models.ForeignKey(DayCare, null=True, on_delete=models.SET_NULL)
    book_date = models.DateField(auto_now=True)
    approval_date = models.DateField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    cancellation_date = models.DateField(blank=True, null=True)
    price_per_day = models.IntegerField()
    status = models.CharField(max_length=1,
                              choices=StatusOptions.choices,
                              default='P'
                              )

    def __str__(self):
        return f"Dog owner ID: {self.dog_owner_id}, daycare ID: {self.daycare_id}, status: {self.status}"

    @classmethod
    def create(cls, dog_owner_id, daycare_id, start_date, end_date, price_per_day, status=StatusOptions.Pending):
        new_order = Order(dog_owner_id=dog_owner_id,
                          daycare_id=daycare_id,
                          book_date=timezone.now(),
                          start_date=start_date,
                          end_date=end_date,
                          price_per_day=price_per_day,
                          status=status
                          )

        new_order.save()
        return new_order

    @staticmethod
    def get_all_dog_owner_orders(dog_owner_id):
        return Order.objects.filter(dog_owner_id=dog_owner_id)

    @staticmethod
    def get_all_daycare_orders(daycare_id):
        return Order.objects.filter(daycare_id=daycare_id)

    @staticmethod
    def get_order_by_order_id(order_id):
        return Order.objects.filter(order_id=order_id.id)

    def approve_order(self):
        if self.status == StatusOptions.Pending:
            self.approval_date = timezone.now()
            self.status = StatusOptions.Approved

        self.save()

    def cancel_order(self):
        if self.status == StatusOptions.Pending or self.status == StatusOptions.Approved:
            self.cancellation_date = timezone.now()
            self.status = StatusOptions.Canceled

        self.save()

    def get_order_total_price(self):
        return self.price_per_day * (self.end_date - self.start_date).days

    @staticmethod
    def get_capacity_of_daycare_in_dates_range(daycare_id, start_date, end_date):
        relevant_orders = Order.objects.filter(daycare_id=daycare_id, status__in=['A', 'O'])
        start_date = datetime.date(year=start_date.year, month=start_date.month, day=start_date.day)
        end_date = datetime.date(year=end_date.year, month=end_date.month, day=end_date.day)
        capacity_per_day_list = [0] * ((end_date - start_date).days + 2)

        for order in relevant_orders:
            if end_date < order.start_date or order.end_date < start_date:
                continue

            number_of_days = (order.end_date - order.start_date).days

            for day in range(number_of_days):
                current_date = order.start_date + datetime.timedelta(days=day)
                if current_date < start_date:
                    continue
                elif current_date > end_date:
                    break
                else:
                    capacity_per_day_list[day] = capacity_per_day_list[day] + 1

        return capacity_per_day_list

    @staticmethod
    def get_all_day_cares_available_on_dates(start_date: str, end_date: str) -> QuerySet:
        start_date = datetime.date.fromisoformat(start_date)
        end_date = datetime.date.fromisoformat(end_date)
        id_list = []
        for day_care in DayCare.objects.all():
            capacity_per_day_list = Order.get_capacity_of_daycare_in_dates_range(day_care.id, start_date, end_date)
            if all(current_capacity < day_care.capacity for current_capacity in capacity_per_day_list):
                id_list.append(day_care.id)
        return DayCare.objects.filter(id__in=id_list)
