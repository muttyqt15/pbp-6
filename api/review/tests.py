from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Review, ReviewImage
from api.authentication.models import Customer
from api.restaurant.models import Restaurant
from .forms import ReviewForm
import json

User = get_user_model()

class ReviewViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Set up test user and customer profile
        self.user = User.objects.create_user(username='testuser', password='password')
        self.customer = Customer.objects.create(user=self.user)
        
        # Set up a restaurant instance
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        
        # Log the user in
        self.client.login(username='testuser', password='password')

        # Set up a test review
        self.review = Review.objects.create(
            customer=self.customer,
            restoran=self.restaurant,
            judul_ulasan="Great place",
            teks_ulasan="I really enjoyed my meal here.",
            penilaian=5,
            display_name="John Doe"
        )
        
    def test_like_review_ajax(self):
        # Test liking a review
        url = reverse('review:like_review_ajax', args=[self.review.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['liked'])
        self.assertEqual(data['total_likes'], 1)

        # Test unliking a review
        response = self.client.post(url)
        data = json.loads(response.content)
        self.assertFalse(data['liked'])
        self.assertEqual(data['total_likes'], 0)

    def test_all_review_view(self):
        # Test retrieving all reviews, ordered by likes and edit time
        url = reverse('review:all_review')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_review.html')
        self.assertIn('all_reviews', response.context)

    def test_main_review_view(self):
        # Test the main review view, showing the logged-in user's reviews
        url = reverse('review:main_review')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_review.html')
        self.assertIn('reviews', response.context)
        self.assertEqual(len(response.context['reviews']), 1)

    def test_create_review(self):
        # Test review creation
        url = reverse('review:create_review')
        data = {
            'judul_ulasan': 'Awesome experience!',
            'teks_ulasan': 'The food was amazing.',
            'penilaian': 4,
            'display_name': 'Anonymous',
            'images': []  # Simulating no images uploaded
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirects after creation
        self.assertEqual(Review.objects.count(), 2)  # New review is created

    def test_edit_review_ajax(self):
        # Test editing a review via AJAX
        url = reverse('review:edit_review_ajax', args=[self.review.id])
        data = {
            'judul_ulasan': 'Updated Review Title',
            'teks_ulasan': 'Updated review text',
            'penilaian': 4,
            'display_name': 'Updated Name'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        
        # Verify the JSON response data
        response_data = json.loads(response.content)
        self.assertEqual(response_data['judul_ulasan'], 'Updated Review Title')
        self.assertEqual(response_data['teks_ulasan'], 'Updated review text')
        self.assertEqual(response_data['penilaian'], 4)

        # Check that the database is updated
        self.review.refresh_from_db()
        self.assertEqual(self.review.judul_ulasan, 'Updated Review Title')
        self.assertEqual(self.review.teks_ulasan, 'Updated review text')
        self.assertEqual(self.review.penilaian, 4)

    def test_delete_review_ajax(self):
        # Test deleting a review via AJAX
        url = reverse('review:delete_review_ajax', args=[self.review.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(Review.objects.count(), 0)  # Review should be deleted

    def test_show_json(self):
        # Test retrieving all reviews as JSON
        url = reverse('review:show_json')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['fields']['judul_ulasan'], 'Great place')

    def test_show_json_by_id(self):
        # Test retrieving a specific review by ID as JSON
        url = reverse('review:show_json_by_id', args=[self.review.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['fields']['judul_ulasan'], 'Great place')