from django.db import models
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
    def create(cls, dog_owner_id, daycare_id, start_date, end_date, price_per_day):
        new_order = Order(dog_owner_id=dog_owner_id,
                          daycare_id=daycare_id,
                          book_date=timezone.now(),
                          start_date=start_date,
                          end_date=end_date,
                          price_per_day=price_per_day,
                          status=StatusOptions.Pending
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

    def get_order_status(self):
        if self.status == StatusOptions.Pending:
            return "Pending"
        elif self.status == StatusOptions.Approved:
            return "Approved"
        elif self.status == StatusOptions.Canceled:
            return "Canceled"
        elif self.status == StatusOptions.OnGoing:
            return "Ongoing"
        return "Finished"

    @staticmethod
    def get_capacity_of_daycare_in_dates_range(daycare_id, start_datetime, end_datetime):
        number_of_days = (end_datetime - start_datetime).days
        capacity_per_day: list[int] = [0] * number_of_days
        start_date = datetime.date(year=start_datetime.year, month=start_datetime.month, day=start_datetime.day)
        end_date = datetime.date(year=end_datetime.year, month=end_datetime.month, day=end_datetime.day)
        relevant_orders = Order.objects.filter(daycare_id=daycare_id,
                                               status__in=['A', 'O'],
                                               end_date__gte=start_date,
                                               start_date__lte=end_date)

        for order in relevant_orders:
            for day in range(number_of_days):
                current_date = order.start_date + datetime.timedelta(days=day)
                if current_date < start_date:
                    continue
                elif current_date > end_date:
                    break
                else:
                    capacity_per_day[day] = capacity_per_day[day] + 1

        return capacity_per_day

    def are_order_dates_available(self):
        capacity_per_day: list[int] = self.get_capacity_of_daycare_in_dates_range(self.daycare_id,
                                                                                  self.start_date,
                                                                                  self.end_date)

        daycare_capacity = DayCare.objects.get(name=self.daycare_id.name).capacity
        return all(current_capacity < daycare_capacity for current_capacity in capacity_per_day)

    def is_the_order_cancelable(self):
        return self.status == StatusOptions.Pending or self.status == StatusOptions.Approved

    def is_the_order_approvable(self):
        return self.status == StatusOptions.Pending and self.are_order_dates_available()
