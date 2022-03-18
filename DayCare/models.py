from django.db import models


class DayCare(models.Model):
    # user_id = models.ForeignKey('user_id', on_delete = models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    price_per_day = models.DecimalField(decimal_places=2, max_digits=10000)
    capacity = models.IntegerField()
    # board_id = models.ForeignKey('board_id', on_delete = models.RESTRICT)
    area = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    adrress = models.CharField(max_length=100)
