from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from dogowner.models import DogOwner
from daycare.models import DayCare


class Review(models.Model):
    review = models.TextField()
    dogowner_id = models.ForeignKey(DogOwner, on_delete=models.SET_NULL, null=True)
    daycare_id = models.ForeignKey(DayCare, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    creation_date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create(review, dogowner_id, daycare_id, rating):
        tmp_review = Review(review=review, dogowner_id=DogOwner.objects.get(id=dogowner_id),
                            daycare_id=DayCare.objects.get(id=daycare_id), rating=rating)

        tmp_review.full_clean()
        tmp_review.save()
        return tmp_review
