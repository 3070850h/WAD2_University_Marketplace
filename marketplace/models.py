from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


# This model stores additional information like profile pictures and account balances.
class UserProfile(models.Model):
    # Links to a standard User instance
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Optional profile picture stored in 'media/profile_images'
    profile_picture = models.ImageField(upload_to="profile_images", blank=True)

    # Virtual currency for transactions. Default is 0.00
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Calculated field for the user's average rating as a seller
    avg_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.username


# Tags: Used for filtering and categorizing products
class Tag(models.Model):
    # Defined primary key
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.tag_name


# Product: Represents an item listed in the marketplace
class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="product_images", blank=True)

    # Foreign Key Relationships. One Tag can be associated with many Products
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    # related_name allows access via user.products_selling
    seller = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="products_selling"
    )

    # Starts as Null and is updated when a transaction occurs.
    buyer = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="products_bought",
    )

    # Tracking listing and purchase times
    list_date = models.DateTimeField(auto_now_add=True)
    purchase_date = models.DateTimeField(null=True, blank=True)

    # Status and Feedback
    rating = models.IntegerField(default=0)

    # determines if the product status is 'Selling'(False) or 'Sold'(True)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Stores simple numerical ratings for sellers
class Review(models.Model):
    # Rating values restricted to 1 through 5
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    # Links the review to a seller to help calculate their avg_rating
    # related_name='received_reviews' allows us to fetch all reviews for a specific user
    seller_reviewed = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="received_reviews"
    )

    def __str__(self):
        return f"Rating: {self.rating} for {self.seller_reviewed.user.username}"
