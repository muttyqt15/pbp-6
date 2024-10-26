from django.db import models
from api.authentication.models import User


class Thread(models.Model):
    id = models.AutoField(
        primary_key=True, editable=False, unique=True, auto_created=True
    )
    content = models.TextField(max_length=456)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="threads")
    image = models.ImageField(upload_to="thread/", null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="likes_thread", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def comment_count(self):
        return self.comments.count()

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def max_length(self):
        return 456

    @property
    def get_comments(self):
        return self.comments.all()

    def __str__(self):
        return self.content if len(self.content) > 50 else f"{self.content[:50]}..."


class Comment(models.Model):
    id = models.AutoField(
        primary_key=True, editable=False, unique=True, auto_created=True
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField(max_length=345)
    likes = models.ManyToManyField(User, related_name="likes_comment", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def get_thread(self):
        return self.thread

    @property
    def max_length(self):
        return
