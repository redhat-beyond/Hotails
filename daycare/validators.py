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


def validate_url_is_image(url):
    img_extenstion = (".gif", ".png", ".jpg", ".jpeg")
    if url:
        if not url.endswith(img_extenstion):
            raise ValidationError("""Invalid URL image - URL should end with '.gif', '.png', '.jpg' or '.jpeg'.""")


def validate_if_daycare_exists(daycare_id):
    from .models import DayCare
    if DayCare.objects.filter(id=daycare_id).exists() is False:
        raise ValidationError("Failed to create image for daycare, the daycare does not exists.")
