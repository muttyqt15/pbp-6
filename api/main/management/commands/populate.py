import random
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from faker import Faker
from api.authentication.models import Customer, User, RestaurantOwner
from api.news.models import Berita
from api.review.models import Review
from api.thread.models import Thread, Comment
from api.restaurant.models import Restaurant, Menu, Food
from api.bookmark.models import Bookmark
from api.user_profile.models import CustomerProfile, OwnerProfile
from api.authentication.constant import Role

fake = Faker()


class Command(BaseCommand):
    help = "Populate dummy data for all models"

    def handle(self, *args, **kwargs):
        # Create users
        users = [
            User.objects.create(
                username=fake.user_name(),
                email=fake.email(),
                role=Role.RESTO_OWNER if num % 2 != 0 else Role.CUSTOMER,
            )
            for num in range(10)
        ]
        customers = [user for user in users if user.role == Role.CUSTOMER]
        owners = [user for user in users if user.role == Role.RESTO_OWNER]

        # Create restaurants
        restaurants = []
        for i in range(5):
            owner = owners[i]
            restaurant = Restaurant.objects.create(
                name=fake.company(),
                district=fake.city(),
                address=fake.address(),
                operational_hours="10:00 - 22:00",
                photo_url=fake.image_url(),
            )
            restaurants.append(restaurant)

        # Create menus for each restaurant
        menus = []
        for restaurant in restaurants:
            for _ in range(3):  # 3 categories per restaurant
                menu = Menu.objects.create(
                    restaurant=restaurant,
                    category=fake.word(),
                )
                menus.append(menu)

        # Create foods for each menu
        foods = []
        for menu in menus:
            for _ in range(5):  # 5 food items per menu
                food = Food.objects.create(
                    menu=menu,
                    name=fake.word(),
                    price=f"{random.randint(10, 100)}.00",
                )
                foods.append(food)

        # Create threads
        threads = []
        for _ in range(5):
            customer = random.choice(customers)
            thread = Thread.objects.create(
                content=fake.text(),
                author=customer,
            )
            threads.append(thread)

        # Create comments for each thread
        comments = []
        for thread in threads:
            for _ in range(3):  # 3 comments per thread
                comment = Comment.objects.create(
                    content=fake.sentence(),
                    thread=thread,
                    author=random.choice(users),
                )
                comments.append(comment)

        # Create reviews for restaurants
        reviews = []
        for restaurant in restaurants:
            for _ in range(5):  # 5 reviews per restaurant
                review = Review.objects.create(
                    judul_ulasan=fake.sentence(),
                    teks_ulasan=fake.text(),
                    display_name=fake.word(),
                    penilaian=random.randint(1, 5),
                    restoran=restaurant,
                    customer=random.choice(customers).customer,
                )
                reviews.append(review)

        # Create news articles
        news_articles = []
        for _ in range(10):
            image_url = fake.image_url()  # Get fake image URL
            image_response = requests.get(image_url)

            if image_response.status_code == 200:
                article = Berita.objects.create(
                    judul=fake.sentence(),
                    konten=fake.text(),
                    author=random.choice(owners).resto_owner,
                )
                # Create a ContentFile and save to the ImageField
                article.image.save(
                    f"{article.judul}.jpg", ContentFile(image_response.content)
                )
                news_articles.append(article)

        # Create bookmarks
        for user in users:
            bookmarked_restaurants = (
                set()
            )  # Keep track of already bookmarked restaurants for this user
            for _ in range(3):
                restaurant = random.choice(restaurants)

                # Ensure the restaurant is not already bookmarked by the user
                while restaurant in bookmarked_restaurants:
                    restaurant = random.choice(restaurants)

                # Add the restaurant to the set and create the bookmark
                bookmarked_restaurants.add(restaurant)
                Bookmark.objects.create(
                    user=user,
                    restaurant=restaurant,
                )

        self.stdout.write(
            self.style.SUCCESS("Successfully populated dummy data for all models!")
        )
