from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from api.restaurant.models import Restaurant
from .models import RestaurantOwner, Customer
from .constant import Role
from .decorators import resto_owner_only, customer_only
from django.http import HttpResponse

User = get_user_model()

# Sample views to test the decorators
@resto_owner_only()
def resto_owner_view(request):
    return HttpResponse("Welcome, Restaurant Owner")


@customer_only()
def customer_view(request):
    return HttpResponse("Welcome, Customer")


class DecoratorTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Create test users for each role
        self.resto_owner_user = User.objects.create_user(
            username="resto_owner",
            email="owner@example.com",
            password="password123",
            role=Role.RESTO_OWNER,
        )
        self.customer_user = User.objects.create_user(
            username="customer_user",
            email="customer@example.com",
            password="password123",
            role=Role.CUSTOMER,
        )

    def test_resto_owner_only_access_granted(self):
        # Test that a restaurant owner can access the view
        request = self.factory.get("/resto_owner/")
        request.user = self.resto_owner_user

        response = resto_owner_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome, Restaurant Owner")

    def test_resto_owner_only_access_denied(self):
        # Test that a customer cannot access the restaurant owner view
        request = self.factory.get("/resto_owner/")
        request.user = self.customer_user

        response = resto_owner_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Access denied. Restaurant owner access only.")

    def test_customer_only_access_granted(self):
        # Test that a customer can access the customer-only view
        request = self.factory.get("/customer/")
        request.user = self.customer_user

        response = customer_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome, Customer")

    def test_customer_only_access_denied(self):
        # Test that a restaurant owner cannot access the customer-only view
        request = self.factory.get("/customer/")
        request.user = self.resto_owner_user

        response = customer_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Access denied. Customer access only.")
