from django.contrib import admin
from django.urls import path
from .views import login, signup, logout, login_flutter, logout_flutter, signup_flutter

app_name = "authentication"
urlpatterns = [
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", logout, name="logout"),
    
    # endpoints for flutter
    path("flogin/", login_flutter, name="flogin"),
    path("fsignup/", signup_flutter, name="fsignup"),
    path("flogout/", logout_flutter, name="flogout"),
]
