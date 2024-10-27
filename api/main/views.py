from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from api.authentication.models import User, RestaurantOwner, Customer
from api.authentication.decorators import resto_owner_only, customer_only
from api.restaurant.models import Restaurant
from api.review.models import Review


def index(request):
    user = request.user
    trending = Restaurant.get_trending_restaurants()
    
    # Check if there are trending restaurants before querying reviews
    reviews = Review.objects.filter(restoran=trending[0]) if trending else None

    # Context for template rendering
    ctx = {
        "user": user,
        "trending": trending,
        "reviews": reviews,
    }
    
    return render(request, "main.html", ctx)


@login_required()
def authenticated_page(request):
    user = User.objects.get(username=request.user)
    if user.is_resto_owner:
        pemilik_toko = RestaurantOwner.get_by_username(user.username)
        data = pemilik_toko
    else:
        customer = Customer.get_by_username(user.username)
        data = customer
    print(data)
    ctx = {"user": user, "data": data}
    return render(request, "authenticated_page.html", ctx)


@resto_owner_only()
def page_resto(request):
    if request.user.is_resto_owner:
        user = "You are a restaurant owner!"
    else:
        user = "You are not a restaurant owner!"
    ctx = {"user": user}
    return render(request, "authenticated_page.html", ctx)


@customer_only()
def page_customer(request):
    if request.user.is_customer:
        user = "You are a customer!"
    else:
        user = "You are not a customer!"

    ctx = {"user": user}
    return render(request, "authenticated_page.html", ctx)
