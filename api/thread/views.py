from .forms import ThreadForm, CommentForm
from .models import Thread, Comment
from django.utils.html import strip_tags
from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
    reverse,
)
from django.contrib.auth.decorators import login_required


def index(request):
    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.user = request.user
            thread.save()
            return redirect(reverse("index"))
    else:
        form = ThreadForm()
    return render(request, "index.html", {"form": form})