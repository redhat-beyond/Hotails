from django.core.exceptions import ObjectDoesNotExist
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

    @staticmethod
    def get_review_by_daycare_id(daycare_id):
        try:
            return Review.objects.filter(daycare_id=daycare_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_average_rating_by_daycare_id(daycare_id):
        reviews = Review.get_review_by_daycare_id(daycare_id)
        if reviews.exists():
            return float("{:.2f}".format(reviews.aggregate(models.Avg('rating'))['rating__avg']))
        return 0
