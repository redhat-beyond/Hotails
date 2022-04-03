from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_username_already_exist(username):
    if User.objects.filter(username=username).exists():
        raise ValidationError("Invalid username")


def validate_max_length(s, length, field):
    if len(s) > length:
        raise ValidationError(f"Invalid {field} - max length is {length}.")


def validate_price(value):
    if isinstance(value, int):
        if len(str(value)) >= 4:
            raise ValidationError("Invalid price - max price is 4 digits.")
    else:
        raise ValidationError("Invalid price_per_day - price should be number.")
