from .models import Comment, Thread
from .forms import CommentForm
from django.utils.html import strip_tags
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
    login_required,
)
from django.contrib.auth.decorators import login_required

