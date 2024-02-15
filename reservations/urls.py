from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="Home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("reserve/<str:id>", views.reserve, name="reserve"),
    path("reservations", views.reservations, name="reservations"),

    #API calls
    path("getAllRestaurants", views.getAllRestaurants, name="getAllRestaurants"),
    path("getReservations", views.getReservations, name="getReservations"),
    path("cancel", views.cancel, name="cancel"),
    path("unarchive", views.unarchive, name="unarchive")
]
