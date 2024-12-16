from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.http import HttpResponseForbidden


def resto_owner_only(redirect_url=None):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_resto_owner:
                return view_func(request, *args, **kwargs)

            if redirect_url:
                return redirect(redirect_url)

            return render(
                request,
                "error.html",
                {"message": "Access denied. Restaurant owner access only."},
            )

        return _wrapped_view

    return decorator


def customer_only(redirect_url=None):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_customer:
                return view_func(request, *args, **kwargs)

            if redirect_url is not None:
                return redirect(redirect_url)

            return render(
                request,
                "error.html",
                {"message": "Access denied. Customer access only."},
            )

        return _wrapped_view

    return decorator


from django.http import JsonResponse


def login_required_json(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(
                {"success": False, "message": "Authentication required."}, status=401
            )
        return view_func(request, *args, **kwargs)

    return wrapper
