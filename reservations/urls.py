from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="Home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #API calls
    path("getAllRestaurants", views.getAllRestaurants, name="getAllRestaurants")
]
