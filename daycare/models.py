from django.db import models
from django.contrib.auth.models import User
from .validators import validate_username_already_exist
from .validators import validate_max_length
from .validators import validate_price
from django.core.validators import validate_email
from django.core.validators import MaxLengthValidator


class DayCare(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, blank=True, null=False, editable=True)
    name = models.CharField(max_length=20, blank=True, unique=True, validators=[MaxLengthValidator])
    description = models.TextField(blank=True, null=True)
    price_per_day = models.IntegerField(blank=False, null=False, default=0)
    capacity = models.IntegerField(null=False, blank=True)
    area = models.CharField(max_length=20, blank=True, validators=[MaxLengthValidator])
    city = models.CharField(max_length=20, blank=True, validators=[MaxLengthValidator])
    address = models.CharField(max_length=50, blank=True, validators=[MaxLengthValidator])

    def __str__(self):
        return self.name

    @staticmethod
    def create(email, username, password, name, description, price_per_day, capacity, area, city, address):
        validate_email(email)
        validate_username_already_exist(username)
        validate_max_length(name, 20, "name")
        validate_max_length(area, 20, "area")
        validate_max_length(city, 20, "city")
        validate_max_length(address, 50, "address")
        validate_price(price_per_day)

        new_daycare = DayCare(user=User.objects.create_user(email=email, username=username, password=password,
                                                            ),
                              name=name, description=description, price_per_day=price_per_day,
                              capacity=capacity, area=area, city=city, address=address)

        new_daycare.user.save()
        new_daycare.save()

        return new_daycare
