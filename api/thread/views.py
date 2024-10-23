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
    login_required,
)
from django.contrib.auth.decorators import login_required

@login_required()
def create_thread(request):
    """Creates a new thread"""
    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)  # Save the form data to the database
            thread.title = strip_tags(thread.title)
            thread.content = strip_tags(thread.content)
            thread.author = request.user
            thread.save()
            return render(
                request, "create_thread.html", {"form": form, "success": True}
            )
    else:
        form = ThreadForm()
    return render(request, "add_thread.html", {"form": form})  # placeholder


@login_required()
def update_thread(request, thread_id):
    """Edit an existing thread"""
    # Retrieve the thread object or return a 404 error if not found
    thread = get_object_or_404(Thread, id=thread_id, author=request.user)

    if request.method == "POST":
        form = ThreadForm(
            request.POST, instance=thread
        )  # Bind the form with existing thread instance
        if form.is_valid():
            thread = form.save(commit=False)
            thread.title = strip_tags(thread.title)  # Strip HTML tags from title
            thread.content = strip_tags(thread.content)  # Strip HTML tags from content
            thread.save()
            return redirect(
                "thread_detail.html"
            )  # Redirect to the thread detail page after saving

    else:
        form = ThreadForm(
            instance=thread
        )  # Populate the form with existing thread data

    return render(request, "edit_thread.html", {"form": form, "thread": thread})


@login_required()
def delete_thread(request, thread_id):
    """Delete a thread"""
    if request.method == "POST":
        thread = get_object_or_404(Thread, id=thread_id, author=request.user)
        thread.delete()
        return JsonResponse(
            {
                "success": True,
                "message": "Thread deleted successfully!",
                "thread_title": thread.title,
            }
        )
    return HttpResponseForbidden()


@login_required()
def get_thread_json_by_id(request, thread_id):
    threads = Thread.objects.filter(id=thread_id, author=request.user)
    data = serializers.serialize("json", threads)
    return HttpResponse(data, content_type="application/json")


def get_thread_json(request):
    threads = Thread.objects.all()
    data = serializers.serialize("json", threads)
    return HttpResponse(data, content_type="application/json")


@login_required()
def create_comment(request):
    """Creates a new comment"""
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # Save the form data to the database
            comment.title = strip_tags(comment.title)
            comment.content = strip_tags(comment.content)
            comment.author = request.user
            comment.save()
            return render(
                request, "create_comment.html", {"form": form, "success": True}
            )
    else:
        form = CommentForm()
    return render(request, "add_comment.html", {"form": form})  # placeholder


@login_required()
def update_comment(request, comment_id):
    """Edit an existing comment"""
    # Retrieve the comment object or return a 404 error if not found
    comment = get_object_or_404(comment, id=comment_id, author=request.user)

    if request.method == "POST":
        form = CommentForm(
            request.POST, instance=comment
        )  # Bind the form with existing comment instance
        if form.is_valid():
            comment = form.save(commit=False)
            comment.title = strip_tags(comment.title)  # Strip HTML tags from title
            comment.content = strip_tags(
                comment.content
            )  # Strip HTML tags from content
            comment.save()
            return redirect(
                "comment_detail.html"
            )  # Redirect to the comment detail page after saving

    else:
        form = CommentForm(
            instance=comment
        )  # Populate the form with existing comment data

    return render(request, "edit_comment.html", {"form": form, "comment": comment})


@login_required()
def delete_comment(request, comment_id):
    """Delete a comment"""
    if request.method == "POST":
        comment = get_object_or_404(comment, id=comment_id, author=request.user)
        comment.delete()
        return JsonResponse(
            {
                "success": True,
                "message": "comment deleted successfully!",
                "comment_title": comment.title,
            }
        )
    return HttpResponseForbidden()


@login_required()
def get_comment_json_by_id(request, comment_id):
    comments = Comment.objects.filter(id=comment_id, author=request.user)
    data = serializers.serialize("json", comments)
    return HttpResponse(data, content_type="application/json")


def get_comment_json(request):
    comments = Comment.objects.all()
    data = serializers.serialize("json", comments)
    return HttpResponse(data, content_type="application/json")
