from django.db import models
from api.authentication.models import User


class Thread(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="threads")
    image = models.ImageField(upload_to="thread/", null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="likes_thread", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_likes_count(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name="likes_comment", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_likes_count(self):
        return self.likes.count()
