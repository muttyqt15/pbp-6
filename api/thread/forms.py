from django import forms
from .models import Thread, Comment


class ThreadForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, required=True, label="Content")
    image = forms.ImageField(required=False, label="Image")

    class Meta:
        model = Thread
        fields = ["content", "image"]


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, required=True, label="Content")

    class Meta:
        model = Comment
        fields = ["content"]
