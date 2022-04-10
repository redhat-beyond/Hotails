from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from enum import Enum


class MaxLength(Enum):
    FIRST_NAME = 15
    LAST_NAME = 15
    DOG_NAME = 15
    DOG_RACE = 30
    DOG_PICTURE_URL = 1000


class ValidateDogOwner:

    def __init__(self, email, username, password, dog_name,
                 first_name, last_name, phone_number,
                 dog_race, dog_picture_url, dog_age,
                 dog_weight, dog_gender):

        self.dog_gender = dog_gender
        self.dog_weight = dog_weight
        self.dog_age = dog_age
        self.dog_picture_url = dog_picture_url
        self.dog_race = dog_race
        self.phone_number = phone_number
        self.last_name = last_name
        self.first_name = first_name
        self.dog_name = dog_name
        self.password = password
        self.username = username
        self.email = email

    def start_validation(self):
        self.validate_dog_owner_username_unique()
        self.validate_dog_gender()
        validate_email(self.email)
        validate_url_is_image(self.dog_picture_url)
        validate_phone(self.phone_number)
        validate_max_length(self.dog_picture_url, MaxLength['DOG_PICTURE_URL'].value, "DOG_PICTURE_URL")
        for i, s in enumerate([self.first_name, self.last_name, self.dog_name, self.dog_race]):
            fields = ["FIRST_NAME", "LAST_NAME", "DOG_NAME", "DOG_RACE"]
            validate_is_alfa(s, fields[i])
            validate_max_length(s, MaxLength[fields[i]].value, fields[i])

    def validate_dog_owner_username_unique(self):
        if User.objects.filter(username=self.username).exists():
            raise ValidationError("Invalid username - username already exist.")

    def validate_dog_gender(self):

        choices = ['M', 'F', 'UN']
        if self.dog_gender not in choices:
            raise ValidationError("Invalid gender - please choose 'M','F' or 'UN.")


def validate_url_is_image(url):
    img_extenstion = (".png", ".jpg", ".jpeg")
    if not url.endswith(img_extenstion):
        raise ValidationError("""Invalid  image URL  - URL should end with '.png', '.jpg' or '.jpeg'.""")


def validate_phone(value):
    if isinstance(value, int):
        if len(str(value)) != 10:
            raise ValidationError("Invalid phone - phone should be 10 digits.")
    else:
        raise ValidationError("Invalid phone - phone should be number.")


def validate_is_alfa(s, field):
    if not all(ch.isalpha() or ch.isspace() for ch in s):
        raise ValidationError(f"Invalid {field} - please enter only alphabet and space characters.")


def validate_max_length(s, length, field):
    if len(s) > length:
        raise ValidationError(f"Invalid {field} - max length is {length}.")
