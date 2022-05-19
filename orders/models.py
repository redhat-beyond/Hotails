from django.db import models
from django.utils import timezone
from daycare.models import DayCare
from dogowner.models import DogOwner


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
