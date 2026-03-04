import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wad2_project.settings")

import django

django.setup()
from django.contrib.auth.models import User
from marketplace.models import UserProfile, Tag, Product, Review
import random


def populate():
    # 1. Create Tags
    tags = ["Textbooks", "Electronics", "Furniture", "Clothing"]
    tag_objs = {}
    for name in tags:
        t = Tag.objects.get_or_create(tag_name=name)[0]
        t.save()
        tag_objs[name] = t
        print(f"- Tag created: {name}")

    # 2. Create Test Users (Email, Username, Password, Balance)
    users_data = [
        {"username": "Alice", "email": "alice@uofg.ac.uk", "balance": 50.00},
        {"username": "Bob", "email": "bob@uofg.ac.uk", "balance": 20.00},
        {"username": "Charlie", "email": "charlie@uofg.ac.uk", "balance": 100.00},
    ]

    user_profiles = []
    for u_data in users_data:
        # Create standard User
        user = User.objects.get_or_create(
            username=u_data["username"], email=u_data["email"]
        )[0]
        # Default password for testing
        user.set_password("password123")  
        user.save()

        # Create UserProfile
        up = UserProfile.objects.get_or_create(user=user)[0]
        up.account_balance = u_data["balance"]
        up.save()
        user_profiles.append(up)
        print(f"- User created: {u_data['username']} (Balance: £{up.account_balance})")

    # 3. Create Products (Selling and Sold)
    products = [
        {
            "name": "Python Textbook",
            "tag": tag_objs["Textbooks"],
            "seller": user_profiles[0],  # Alice
            "price": 35.00,
            "description": "Essential for second year students. No highlights.",
            "is_sold": False,
        },
        {
            "name": "Camera",
            "tag": tag_objs["Electronics"],
            "seller": user_profiles[1],  # Bob
            "price": 12.00,
            "description": "Adjustable arm, warm light included.",
            "is_sold": True,  # This one is sold
            "buyer": user_profiles[2],  # Bought by Charlie
        },
        {
            "name": "Second-hand rice cooker",
            "tag": tag_objs["Electronics"],
            "seller": user_profiles[0],  # Alice
            "price": 8.00,
            "description": "Used but works perfectly.",
            "is_sold": False,
        },
    ]

    for p_data in products:
        p = Product.objects.get_or_create(
            name=p_data["name"],
            tag=p_data["tag"],
            seller=p_data["seller"],
            price=p_data["price"],
            description=p_data["description"],
        )[0]

        p.is_sold = p_data.get("is_sold", False)
        if p.is_sold:
            p.buyer = p_data["buyer"]
            # Logic simulation: If sold, seller gets the money
            p.seller.account_balance += p.price
            p.seller.save()

        p.save()
        print(f"- Product created: {p.name} (Sold: {p.is_sold})")

    # 4. Create Sample Reviews
    # Adding a rating to Bob because he sold a lamp
    add_review(user_profiles[1], 5)
    add_review(user_profiles[1], 4)

    # Update Avg Rating for Bob
    update_avg_rating(user_profiles[1])


def add_review(seller, rating_value):
    r = Review.objects.get_or_create(seller_reviewed=seller, rating=rating_value)[0]
    r.save()


def update_avg_rating(profile):
    reviews = Review.objects.filter(seller_reviewed=profile)
    if reviews.exists():
        total = sum([r.rating for r in reviews])
        profile.avg_rating = total / reviews.count()
        profile.save()
        print(f"- Updated Avg Rating for {profile.user.username}: {profile.avg_rating}")


if __name__ == "__main__":
    print("--- Starting Population Script ---")
    populate()
    print("--- Population Complete ---")
