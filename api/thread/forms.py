from django import forms
from .models import Thread, Comment


class ThreadForm(forms.ModelForm):
    title = forms.CharField(max_length=200, required=True, label="Title")
    content = forms.CharField(widget=forms.Textarea, required=True, label="Content")
    image = forms.ImageField(required=False, label="Image")

    class Meta:
        model = Thread
        fields = ["title", "content", "image"]


class CommentForm(forms.ModelForm):
    title = forms.CharField(max_length=200, required=True, label="Title")
    content = forms.CharField(widget=forms.Textarea, required=True, label="Content")

    class Meta:
        model = Comment
        fields = ["title", "content"]
