from django.test import TestCase, Client
from django.urls import reverse
from .models import Restaurant, Menu, Food
from django.contrib.auth.models import User
from django.http import JsonResponse
from api.authentication.models import RestaurantOwner, User, Customer
import json

class RestaurantViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.restaurant_owner = RestaurantOwner.objects.create(user=self.user)
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            district='Test District',
            address='Test Address',
            operational_hours='9 AM - 9 PM',
            photo_url='https://placehold.co/600x400',
            restaurantowner=self.restaurant_owner
        )
        self.menu = Menu.objects.create(restaurant=self.restaurant, category='Test Category')
        self.food = Food.objects.create(menu=self.menu, name='Test Food', price=10000)

    def test_restaurant_view(self):
        response = self.client.get(reverse('restaurant', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.restaurant.name)
        self.assertContains(response, self.restaurant.district)
        self.assertContains(response, self.restaurant.address)
        self.assertContains(response, self.restaurant.operational_hours)

    def test_menu_view(self):
        response = self.client.get(reverse('menu_view', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.menu.category)
        self.assertContains(response, self.food.name)
        self.assertContains(response, self.food.price)

    def test_edit_restaurant(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('edit_restaurant', args=[self.restaurant.id]), {
            'name': 'Updated Restaurant',
            'district': 'Updated District',
            'address': 'Updated Address',
            'operational_hours': '10 AM - 10 PM'
        })
        self.assertEqual(response.status_code, 200)
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.name, 'Updated Restaurant')
        self.assertEqual(self.restaurant.district, 'Updated District')
        self.assertEqual(self.restaurant.address, 'Updated Address')
        self.assertEqual(self.restaurant.operational_hours, '10 AM - 10 PM')

    def test_add_menu(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_menu'), {
            'category': 'New Category',
            'restaurant_id': self.restaurant.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Menu.objects.filter(category='New Category').exists())

    def test_add_food(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_food'), {
            'name': 'New Food',
            'price': 20000,
            'menu_id': self.menu.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Food.objects.filter(name='New Food').exists())

    def test_filter_restaurants(self):
        response = self.client.post(reverse('filter_restaurants'), json.dumps({
            'search': 'Test',
            'sort_by': 'name'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.restaurant.name)

    def test_get_restaurant_menu(self):
        response = self.client.get(reverse('get_restaurant_menu', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.food.name)

    def test_get_restaurant_xml(self):
        response = self.client.get(reverse('get_restaurant_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/xml', response['Content-Type'])

    def test_get_restaurants_xml_by_id(self):
        response = self.client.get(reverse('get_restaurants_xml_by_id', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/xml', response['Content-Type'])

    def test_get_restaurants_json(self):
        response = self.client.get(reverse('get_restaurants_json'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response['Content-Type'])

    def test_get_restaurants_json_by_id(self):
        response = self.client.get(reverse('get_restaurants_json_by_id', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response['Content-Type'])