from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="Home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("reserve/<str:id>", views.reserve, name="reserve"),

    #API calls
    path("getAllRestaurants", views.getAllRestaurants, name="getAllRestaurants")
]
