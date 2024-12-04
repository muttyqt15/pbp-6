from django.contrib import admin
from django.urls import path
from .views import index, authenticated_page, page_resto, page_customer

app_name = "main"

urlpatterns = [
    path("", index, name="index"),
    path("test", authenticated_page, name="test"),
    path("customer", page_customer, name="customer"),
    path("resto_owner", page_resto, name="resto_owner"),
]
