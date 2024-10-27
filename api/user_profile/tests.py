from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from api.user_profile.models import CustomerProfile, OwnerProfile
from api.authentication.models import Customer, RestaurantOwner
from django.contrib.messages import get_messages

class UserProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer_user = User.objects.create_user(
            username='customeruser', password='password123', is_customer=True
        )
        self.owner_user = User.objects.create_user(
            username='owneruser', password='password123', is_resto_owner=True
        )
        self.customer_profile = CustomerProfile.objects.create(user=self.customer_user)
        self.owner_profile = OwnerProfile.objects.create(user=self.owner_user)

    def test_profile_view_customer(self):
        self.client.login(username='customeruser', password='password123')
        response = self.client.get(reverse('profile_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_profile.html')
        self.assertIn('customer_profile', response.context)
        self.assertIsNone(response.context['owner_profile'])

    def test_profile_view_owner(self):
        self.client.login(username='owneruser', password='password123')
        response = self.client.get(reverse('profile_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_profile.html')
        self.assertIn('owner_profile', response.context)
        self.assertIsNone(response.context['customer_profile'])

    def test_edit_profile_success(self):
        self.client.login(username='customeruser', password='password123')
        response = self.client.post(reverse('edit_profile'), {
            'username': 'updateduser',
            'bio': 'This is the updated bio',
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content, 
            {
                'success': True,
                'updated_username': 'updateduser',
                'updated_bio': 'This is the updated bio',
            }
        )

    def test_edit_profile_invalid(self):
        self.client.login(username='customeruser', password='password123')
        response = self.client.post(reverse('edit_profile'), {
            'username': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json())
        self.assertFalse(response.json()['success'])
        self.assertIn('errors', response.json())

    def test_delete_account(self):
        self.client.login(username='customeruser', password='password123')
        response = self.client.post(reverse('delete_account'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        with self.assertRaises(CustomerProfile.DoesNotExist):
            CustomerProfile.objects.get(user=self.customer_user)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='customeruser')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Your account has been successfully deleted.")
