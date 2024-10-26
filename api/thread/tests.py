from django.test import TestCase, Client
from api.authentication.models import User
from .models import Thread, Comment


class ThreadModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.thread = Thread.objects.create(
            content="This is a test thread.", author=self.user
        )

    def test_thread_creation(self):
        self.assertIsInstance(self.thread, Thread)
        self.assertEqual(self.thread.content, "This is a test thread.")
        self.assertEqual(self.thread.author, self.user)

    def test_thread_like(self):
        self.thread.likes.add(self.user)
        self.assertEqual(self.thread.like_count, 1)
        self.thread.likes.remove(self.user)
        self.assertEqual(self.thread.like_count, 0)

    def test_thread_delete(self):
        self.thread.delete()
        self.assertEqual(Thread.objects.count(), 0)


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.thread = Thread.objects.create(
            content="This is a test thread.", author=self.user
        )
        self.comment = Comment.objects.create(
            content="This is a test comment.", author=self.user, thread=self.thread
        )

    def test_comment_creation(self):
        self.assertIsInstance(self.comment, Comment)
        self.assertEqual(self.comment.content, "This is a test comment.")
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.thread, self.thread)

    def test_comment_like(self):
        self.comment.likes.add(self.user)
        self.assertEqual(self.comment.like_count, 1)
        self.comment.likes.remove(self.user)
        self.assertEqual(self.comment.like_count, 0)

    def test_comment_delete(self):
        self.comment.delete()
        self.assertEqual(Comment.objects.count(), 0)
