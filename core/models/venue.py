from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import UniqueConstraint, Q, functions
import logging


class Country(models.Model):
    name = models.CharField(max_length=100)

    class meta:
        constraints = [
            UniqueConstraint(
                name='unique_country_name',
                fields=[functions.Lower('name')],
                condition=Q(name__isnull=False),
            )
        ]


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class Venue(models.Model):
    name = models.CharField(max_length=255)
    location = models.PointField(geography=True, null=True, blank=True)
    address = models.CharField(max_length=511, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rental_price = models.DecimalField(max_digits=8, decimal_places=2,
                                       validators=[MinValueValidator(0.00)])
    landlord = models.ForeignKey(User, on_delete=models.CASCADE)
    amenities = models.JSONField(default=dict, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    images = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):

    def custom_behavior(self, *args, **kwargs):
        logging.warning(f"{self}, {args}, {kwargs}")
        logging.warning(f"{args[1]}")
        review_obj = args[1].get()
        review_obj.venue = None
        review_obj.save()
        logging.warning(f"{'#'*50}")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1,
                                 validators=[MinValueValidator(0.0),
                                             MaxValueValidator(5.0)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
