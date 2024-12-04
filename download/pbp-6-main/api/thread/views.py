from .forms import ThreadForm, CommentForm
from .models import Thread, Comment
import json
from django.utils.html import strip_tags
from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt


@login_required()
def index(request):
    if request.method == "POST":
        form = ThreadForm(request.POST, request.FILES)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect('/thread')
    else:
        form = ThreadForm()
    threads = Thread.objects.all()
    return render(
        request, "index.html", {"form": form, "threads": threads, "user": request.user}
    )

@login_required()
@require_http_methods(["POST", "GET"])
def like_thread(request, id):
    if request.method == "POST":
        thread = get_object_or_404(Thread, id=id)
        status_liked = request.user in thread.likes.all()
        if status_liked:  # O(n), is this ok?
            thread.likes.remove(request.user)
        else:
            thread.likes.add(request.user)
        return JsonResponse({"likes": thread.like_count, "liked": status_liked})
    return HttpResponseForbidden()

@login_required()
@require_http_methods(["POST", "GET"])
def like_comment(request, comment_id):
    if request.method == "POST":
        comment = get_object_or_404(Comment, id=comment_id)
        status_liked = request.user in comment.likes.all()
        if status_liked:  # O(n), is this ok?
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
        return JsonResponse({"likes": comment.like_count, "liked": status_liked})
    return HttpResponseForbidden()

@login_required()
@require_http_methods(["POST", "GET"])
def delete_thread(request, id):
    thread = get_object_or_404(Thread, id=id)
    if request.user == thread.author:
        thread.delete()
        return JsonResponse(
            {
                "message": "Thread deleted successfully.",
                "status": "success",
                "success": True,
            }
        )
    else:
        return JsonResponse(
            {
                "message": "You are not authorized to delete this thread.",
                "status": "error",
                "success": False,
            }
        )

@login_required()
@require_http_methods(["POST", "GET"])
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    if request.user == comment.author:
        comment.delete()
        return JsonResponse(
            {
                "message": "Comment deleted successfully.",
                "status": "success",
                "success": True,
            }
        )
    else:
        return JsonResponse(
            {
                "message": "You are not authorized to delete this comment.",
                "status": "error",
                "success": False,
            }
        )


@login_required
@require_http_methods(["POST", "GET"])
@csrf_exempt
def edit_thread(request, id):
    thread = get_object_or_404(Thread, id=id)

    if request.method == "POST":
        # Parse JSON data from request body
        data = json.loads(request.body)

        # Ensure you get all required fields, including content and any other required fields
        content = data.get("content", None)

        # Strip HTML tags if content is provided
        if content:
            content = strip_tags(content)

        # Create a dictionary of data for the form
        form_data = {
            "content": content,
            "image": data.get("image", None),
        }

        # Create the form instance with the populated data
        form = ThreadForm(form_data, request.FILES, instance=thread)

        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return JsonResponse(
                {
                    "message": "Thread edited successfully.",
                    "status": "success",
                    "success": True,
                    "data": {
                        "content": thread.content,
                        "image": thread.image.url if thread.image else None,
                    },
                }
            )
        else:
            return JsonResponse(
                {
                    "message": "Thread edit failed.",
                    "status": "error",
                    "success": False,
                    "error": form.errors,
                    "test": data,  # Include the original data for debugging
                }
            )
    else:
        form = ThreadForm(instance=thread)
        return JsonResponse(
            {
                "message": "Editing in process",
                "form": form,
                "data": {
                    "content": thread.content,
                    "image": thread.image.url if thread.image else None,
                },
            }
        )


@login_required()
def detail_thread(request, id):
    thread = get_object_or_404(Thread, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.thread = thread
            comment.save()
            return redirect("/thread", id=id)
        else:
            return redirect("main:test")
    else:
        form = CommentForm()
    comments = thread.comments.all()
    return render(
        request,
        "detail_thread.html",
        {"thread": thread, "comments": comments, "user": request.user, "form": form},
    )
