from django.contrib.auth.models import AbstractUser
from django.db import models


class Listing(models.Model):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=256)
    price = models.FloatField(max_length=64)
    listed_by = models.CharField(max_length=64)
    category = models.CharField(max_length=64)

    image = models.ImageField(upload_to='images/', null=True, blank=True, default='images/no_photo.jpg')

    winner = models.CharField(max_length=64, default="No winner")
    def __str__(self):
        return f"{self.id}: {self.name} at price {self.price}"


class Bid(models.Model):
    bidder = models.CharField(max_length=64)
    amount = models.FloatField(max_length=64)

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing_bids', default=1)

    def __str__(self):
        return f"{self.id}: ${self.amount} by {self.bidder}"

class Comment(models.Model):
    user = models.CharField(max_length=64)
    comment = models.TextField(max_length=256)


class User(AbstractUser):
    watched_listings = models.ManyToManyField(Listing, blank=True, related_name="watchers")

