from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from api.news.models import Berita
from api.authentication.models import RestaurantOwner, User
from api.authentication.constant import Role
from api.news.forms import BeritaEntryForm
from PIL import Image
import io
import uuid

class BeritaModelTest(TestCase):
    def setUp(self):
        # Set up test user and restaurant owner
        self.user = User.objects.create_user(
            username="testuser",
            email="owner@example.com",
            password="password",
            role=Role.RESTO_OWNER,
        )
        self.restaurant_owner = RestaurantOwner.objects.create(user=self.user)

        # Set up test article
        self.berita = Berita.objects.create(
            author=self.restaurant_owner,
            judul="Test Berita",
            konten="This is a test content"
        )

    def test_berita_creation(self):
        """Test the creation of a Berita object"""
        berita_count = Berita.objects.count()
        self.assertEqual(berita_count, 1)
        self.assertEqual(self.berita.judul, "Test Berita")
        self.assertEqual(self.berita.konten, "This is a test content")

    def test_like_berita(self):
        """Test liking and unliking a Berita"""
        self.berita.like.add(self.user)
        self.assertEqual(self.berita.like_count, 1)
        
        # Unlike the Berita
        self.berita.like.remove(self.user)
        self.assertEqual(self.berita.like_count, 0)

    def test_default_timestamps(self):
        """Test default timestamps are set correctly on creation"""
        self.assertIsNotNone(self.berita.tanggal)
        self.assertIsNotNone(self.berita.tanggal_pembaruan)
        self.assertEqual(self.berita.tanggal, self.berita.tanggal_pembaruan)


class BeritaFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "judul": "<h1>Test Title</h1>",
            "konten": "<p>Test content with HTML tags</p>"
        }

    def test_form_cleaning(self):
        """Test that the form strips HTML tags from input fields"""
        form = BeritaEntryForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["judul"], "Test Title")
        self.assertEqual(form.cleaned_data["konten"], "Test content with HTML tags")


class BeritaViewsTest(TestCase):
    def setUp(self):
        # Create test user and set as restaurant owner
        self.client = Client()
        
        self.user = User.objects.create_user(
            username="testuser",
            email="owner@example.com",
            password="password",
            role=Role.RESTO_OWNER,
        )
        self.restaurant_owner = RestaurantOwner.objects.create(user=self.user)
    
        # Login with client
        self.client.login(username="testuser", password="password")

        # Create a test Berita
        self.berita = Berita.objects.create(
            author=self.restaurant_owner,
            judul="Test Berita",
            konten="This is a test content"
        )

    def test_show_main(self):
        """Test the show_main view"""
        response = self.client.get(reverse("news:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main_berita.html")

    def test_owner_panel_authorization(self):
        """Test owner_panel view access for authorized and unauthorized users"""
        response = self.client.get(reverse("news:owner_panel"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "owner_panel.html")

        # Test unauthorized access by logging out
        self.client.logout()
        response = self.client.get(reverse("news:owner_panel"))
        self.assertEqual(response.status_code, 302)  

    def test_add_berita_ajax(self):
        """Test adding a new Berita with AJAX"""
        response = self.client.post(
            reverse("news:add_berita_ajax"),
            {"judul": "New Berita", "konten": "New content"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Berita.objects.filter(judul="New Berita").exists())

    def test_edit_berita(self):
        """Test editing an existing Berita"""
        new_judul = "Updated Test Berita"
        response = self.client.post(
            reverse("news:edit_berita", args=[self.berita.id]),
            {"judul": new_judul, "konten": self.berita.konten}
        )
        self.assertEqual(response.status_code, 200)
        self.berita.refresh_from_db()
        self.assertEqual(self.berita.judul, new_judul)

    def test_delete_berita(self):
        """Test deleting an existing Berita"""
        response = self.client.get(reverse("news:delete_berita", args=[self.berita.id]))
        self.assertFalse(Berita.objects.filter(id=self.berita.id).exists())
        self.assertEqual(response.status_code, 302)

    def test_like_berita_view(self):
        """Test liking and unliking a Berita via the like_berita view"""
        response = self.client.post(reverse("news:like_berita", args=[self.berita.id]))
        self.berita.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.berita.like_count, 1)

        # Test unliking the Berita
        response = self.client.post(reverse("news:like_berita", args=[self.berita.id]))
        self.berita.refresh_from_db()
        self.assertEqual(self.berita.like_count, 0)

    def test_invalid_berita_edit(self):
        """Test editing a non-existent Berita returns an error"""
        invalid_id = uuid.uuid4()
        response = self.client.post(
            reverse("news:edit_berita", args=[invalid_id]),
            {"judul": "Nonexistent", "konten": "Content"}
        )
        self.assertEqual(response.status_code, 404)

    def test_image_upload(self):
        """Test image upload handling in Berita creation and edit"""

        # Create a temporary in-memory image file
        image = io.BytesIO()
        Image.new("RGB", (100, 100)).save(image, format="JPEG")
        image.seek(0)
        uploaded_image = SimpleUploadedFile("test_image.jpg", image.read(), content_type="image/jpeg")

        # Send POST request with image
        response = self.client.post(
            reverse("news:add_berita_ajax"),
            {"judul": "Image Berita", "konten": "Content with image", "gambar": uploaded_image},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Berita.objects.filter(judul="Image Berita").exists())