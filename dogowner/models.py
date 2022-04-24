from django.db import models
from django.contrib.auth.models import User
from .validators import ValidateDogOwner, MaxLength


class Gender(models.TextChoices):
    Male = 'M', 'Male'
    Female = 'F', 'Female'
    Unknown = 'UN', 'Unknown'


class DogOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=MaxLength['FIRST_NAME'].value, blank=True)
    last_name = models.CharField(max_length=MaxLength['LAST_NAME'].value, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    dog_name = models.CharField(max_length=MaxLength['DOG_NAME'].value, blank=True)
    dog_race = models.CharField(max_length=MaxLength['DOG_RACE'].value, blank=True)
    dog_picture_url = models.URLField(max_length=MaxLength['DOG_PICTURE_URL'].value, blank=True)
    dog_age = models.IntegerField(null=True, blank=True)
    dog_weight = models.FloatField(null=True, blank=True)
    dog_gender = models.CharField(
        max_length=2,
        choices=Gender.choices,
        default='UN', blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @staticmethod
    def create(email, username, password, dog_name,
               first_name, last_name, phone_number,
               dog_race, dog_picture_url, dog_age,
               dog_weight, dog_gender):

        ValidateDogOwner(email, username, password, dog_name,
                         first_name, last_name, phone_number,
                         dog_race, dog_picture_url, dog_age,
                         dog_weight, dog_gender).start_validation()

        new_dog_owner = DogOwner(user=User.objects.create_user(username=username,
                                                               email=email,
                                                               password=password
                                                               ),
                                 first_name=first_name,
                                 last_name=last_name,
                                 phone_number=phone_number,
                                 dog_name=dog_name,
                                 dog_race=dog_race,
                                 dog_picture_url=dog_picture_url,
                                 dog_age=dog_age,
                                 dog_weight=dog_weight,
                                 dog_gender=dog_gender
                                 )

        new_dog_owner.user.save()
        new_dog_owner.save()
        return new_dog_owner
