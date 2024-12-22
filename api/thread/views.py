from .forms import ThreadForm, CommentForm
from .models import Thread, Comment
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
from api.user_profile.models import CustomerProfile, OwnerProfile
from django.core.files.base import ContentFile
from api.authentication.decorators import login_required_json
import base64
import json


@login_required()
def index(request):
    if request.method == "POST":
        form = ThreadForm(request.POST, request.FILES)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect("/thread")
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

def fget_thread(request):
    try:
        # Fetch threads and related author information
        threads = Thread.objects.select_related("author").order_by("-created_at")
        # Construct the response with additional author details
        thread_list = []
        for thread in threads:
            author = thread.author
            author_profile = None

            # Check if the author is a Customer or RestaurantOwner and fetch the profile
            if hasattr(author, "customer"):
                # Author is a Customer, get their profile
                author_profile = CustomerProfile.objects.filter(
                    user=author.customer
                ).first()
            elif hasattr(author, "resto_owner"):
                # Author is a RestaurantOwner, get their profile
                author_profile = OwnerProfile.objects.filter(
                    user=author.resto_owner
                ).first()

            if request.user.is_authenticated:
                # check if liked by user
                liked = thread.likes.filter(id=request.user.id).exists()
            thread_list.append(
                {
                    "id": thread.id,
                    "content": thread.content,
                    "created_at": thread.created_at,
                    "updated_at": thread.updated_at,
                    "author_id": author.id,
                    "author_name": author.username,
                    "author_profile_pic": (
                        author_profile.profile_pic.url
                        if author_profile and author_profile.profile_pic
                        else None
                    ),
                    "image": thread.image.url if thread.image else None,
                    "comment_count": thread.comments.count(),
                    "likes_count": thread.likes.count(),
                    "liked": liked,
                }
            )

        return JsonResponse(
            {
                "success": True,
                "message": "Threads successfully fetched!",
                "threads": thread_list,
            },
        )
    except Exception as e:
        (e)
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def fcreate_thread(request):
    try:
        data = json.loads(request.body)
        form = ThreadForm(data)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            if "image" in data and data["image"]:
                image_data = data.pop("image")
                format, imgstr = image_data.split(
                    ";base64,"
                )  # Extract base64 and format
                ext = format.split("/")[-1]  # Get file extension (e.g., png, jpg)
                # Decode base64 image if present
                image_file = ContentFile(
                    base64.b64decode(imgstr), name=f"thread_image.{ext}"
                )
                thread.image = image_file
            thread.save()
            return JsonResponse(
                {
                    "success": True,
                    "message": "Thread created successfully.",
                    "data": {
                        "id": thread.id,
                        "content": thread.content,
                        "image": thread.image.url if thread.image else None,
                        "likes": thread.like_count,
                    },
                },
                status=201,
            )
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


# Like a thread (Flutter-specific)
@login_required_json
@csrf_exempt
@require_http_methods(["POST"])
def flike_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    liked = request.user in thread.likes.all()
    if liked:
        thread.likes.remove(request.user)
    else:
        thread.likes.add(request.user)
    return JsonResponse(
        {"success": True, "liked": not liked, "likes": thread.like_count}, status=200
    )


# Delete a thread (Flutter-specific)
@login_required_json
@csrf_exempt
def fdelete_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.user == thread.author:
        thread.delete()
        return JsonResponse(
            {"success": True, "message": "Thread deleted successfully."}
        )
    else:
        return JsonResponse(
            {"success": False, "message": "Not authorized."}, status=403
        )


# Edit a thread (Flutter-specific)
@login_required_json
@csrf_exempt
def fedit_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    try:
        data = json.loads(request.body)
        content = strip_tags(data.get("content", thread.content))
        form = ThreadForm({"content": content}, instance=thread)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return JsonResponse(
                {
                    "success": True,
                    "message": "Thread updated successfully.",
                    "data": {
                        "id": thread.id,
                        "content": thread.content,
                        "image": thread.image.url if thread.image else None,
                        "likes": thread.like_count,
                    },
                },
                status=200,
            )
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


# Get thread details (Flutter-specific)
@csrf_exempt
@require_http_methods(["GET"])
def fget_thread_details(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    # Fetch threads and related author information
    comments = Comment.objects.filter(thread=thread).select_related("author").order_by("-created_at")
    # Construct the response with additional author details
    comment_list = []
    for comment in comments:
        author = comment.author
        author_profile = None

        # Check if the author is a Customer or RestaurantOwner and fetch the profile
        if hasattr(author, "customer"):
            # Author is a Customer, get their profile
            author_profile = CustomerProfile.objects.filter(
                user=author.customer
            ).first()
        elif hasattr(author, "resto_owner"):
            # Author is a RestaurantOwner, get their profile
            author_profile = OwnerProfile.objects.filter(
                user=author.resto_owner
            ).first()

        if request.user.is_authenticated:
            # check if liked by user
            liked = comment.likes.filter(id=request.user.id).exists()
        comment_list.append(
            {
                "id": comment.id,
                "content": comment.content,
                "created_at": comment.created_at,
                "updated_at": comment.updated_at,
                "author_id": author.id,
                "author_name": author.username,
                "author_profile_pic": (
                    author_profile.profile_pic.url
                    if author_profile and author_profile.profile_pic
                    else None
                ),
                "likes_count": comment.likes.count(),
                "liked": liked,
            }
        )
    return JsonResponse(
        {
            "success": True,
            "data": {
                "thread": {
                    "id": thread.id,
                    "content": thread.content,
                    "image": thread.image.url if thread.image else None,
                    "likes": thread.like_count,
                },
                "comments": comment_list,
            },
        }
    )


# Add a comment to a thread (Flutter-specific)
@login_required_json
@csrf_exempt
@require_http_methods(["POST"])
def fadd_comment(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    try:
        data = json.loads(request.body)
        content = strip_tags(data.get("content"))
        form = CommentForm({"content": content})
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.thread = thread
            comment.save()
            return JsonResponse(
                {
                    "success": True,
                    "message": "Comment added successfully.",
                    "data": {
                        "id": comment.id,
                        "content": comment.content,
                        "likes": comment.like_count,
                    },
                },
                status=201,
            )
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


# Like a comment (Flutter-specific)
@login_required_json
@csrf_exempt
@require_http_methods(["POST"])
def flike_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    liked = request.user in comment.likes.all()
    if liked:
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return JsonResponse(
        {"success": True, "liked": not liked, "likes": comment.like_count}, status=200
    )


# Delete a comment (Flutter-specific)
@login_required_json
@csrf_exempt
def fdelete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author:
        comment.delete()
        return JsonResponse(
            {"success": True, "message": "Comment deleted successfully."}, status=200
        )
    else:
        return JsonResponse(
            {"success": False, "message": "Not authorized to delete comment."},
            status=403,
        )
