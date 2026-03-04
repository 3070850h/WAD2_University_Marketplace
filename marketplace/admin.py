from django.contrib import admin
from marketplace.models import UserProfile, Tag, Product, Review


# User Profile Admin: Monitor balances and ratings
class UserProfileAdmin(admin.ModelAdmin):
    # Display key user metrics in the list view
    list_display = ("user", "profile_picture", "account_balance", "avg_rating")


# Tag Admin: Manage categories
class TagAdmin(admin.ModelAdmin):
    list_display = ("tag_name",)
    search_fields = ("tag_name",)


# Product Admin: Track marketplace activity
class ProductAdmin(admin.ModelAdmin):
    # Shows the most important info: Name, Price, Seller, and Status
    list_display = ("name", "seller", "price", "is_sold", "list_date")
    # Filter by tags or sold status on the right sidebar
    list_filter = ("is_sold", "tag")
    # Search by product name
    search_fields = ("name",)
    # Automatically organizes by the newest listings
    ordering = ("-list_date",)


# Review Admin: Check buyer feedback
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("seller_reviewed", "rating")
    list_filter = ("rating",)


# Register all models to the Django Admin site
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
