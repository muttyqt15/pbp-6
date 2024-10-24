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


@login_required()
def index(request):
    if request.method == "POST":
        form = ThreadForm(request.POST, request.FILES)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect("main:index")
    else:
        form = ThreadForm()
    threads = Thread.objects.all()
    print(request.user.id)
    print([[thread.image.url, thread.author.id] for thread in threads if thread.image], 'hei')
    return render(request, "index.html", {"form": form, "threads": threads, "user": request.user})
