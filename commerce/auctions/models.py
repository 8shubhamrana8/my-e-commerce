from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime

class User(AbstractUser):
    pass

class Listing(models.Model):

    class categories(models.IntegerChoices):
        FASHION = 1 , 'Fashion'
        ELECTRONICS = 2 , 'Electronics'
        HOME = 3 , 'Home'
        TOYS = 4 , 'Toys'
    
    category = models.IntegerField(choices=categories)
    title = models.CharField(max_length=50)
    description = models.TextField(null=False)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)],
        null= True,
        default=0
    )
    placed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=500, default='/static/auctions/default_cat.png')
    isActive = models.BooleanField(default=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    
    @property
    def highestBid(self):
        highest_bid = self.bids.order_by('-amount').first()
        if highest_bid:
            return highest_bid.amount
        else:
            return self.price

    def __str__(self):
        return f"{self.title} listing by {self.placed_by} starting {self.price}"


class Bid(models.Model):
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        )
    
    listing = models.ForeignKey(
        Listing, 
        on_delete=models.CASCADE, 
        related_name="bids"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )


class Comment(models.Model):

    author = models.ForeignKey(
        User,
        on_delete = models.CASCADE
    )
    listing = models.ForeignKey(
        Listing,
        on_delete = models.CASCADE,
        blank = True,
        null=True,
        related_name= "comments"
    ) 
    comment = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def formatted_time(self):
        if self.timestamp:
            return self.timestamp.strftime("%d %B at %I%p").lower()
        return "unknown time"

    def __str__(self):
        return f'''
                {self.author}: 
                    {self.comment} {self.formatted_time}'''