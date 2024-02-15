import datetime

from django.utils import timezone
from datetime import time
import json
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.mail import send_mail
from django.utils.dateparse import parse_datetime

# Create your views here.


def index(request):
    return render(request, "reservations/index.html")


def reservations(request):
    return render(request, "reservations/reservations.html")


def reserve(request, id):
    # If request is GET means the user is filling the reservation form
    if request.method == "GET":
        if request.user.is_authenticated:
            restaurant = Restaurant.objects.get(id=id)
            return render(
                request,
                "reservations/reserve.html",
                {"restaurant": restaurant},
            )
        else:
            return HttpResponseRedirect(reverse("login"))
    # If request is POST means the user is clicked save and we create the reservation
    else:
        restaurant = Restaurant.objects.get(id=id)
        shifts = Shift.objects.filter(restaurant=restaurant)
        # Getting time from reserve form and convert it to a timezone aware time
        timestr = request.POST["time"]
        parsed_time = datetime.datetime.strptime(timestr, "%H:%M").time()
        current_date = datetime.date.today()
        mydatetime = datetime.datetime.combine(current_date, parsed_time)
        current_time = timezone.localtime(timezone.now()).time()
        numberOfDiners = request.POST["numberOfDiners"]

        # Opening and closing times of all restaurants
        min = time(10, 0)
        max = time(23, 0)
        
        # If reservation time is earlier than current time retunr to reserve with an alert
        if parsed_time <= current_time:
            return render(
                request,
                "reservations/reserve.html",
                {"restaurant": restaurant, "alert": "Old time"},
            )

        # if restaurant is open
        if min <= parsed_time <= max:
            # look for the shift range based on time entered
            for shift in shifts:
                # converting first 2 digits of the hour to int to check if the time fits into shift range
                shiftSubs = int(shift.shiftRange[0:2])
                timeSubs = int(timestr[0:2])
                if shiftSubs == timeSubs or shiftSubs == timeSubs - 1:
                    # Check if shift for that restaurant is full
                    if shift.isFull:
                        return render(
                            request,
                            "reservations/reserve.html",
                            {"restaurant": restaurant, "alert": "Full"},
                        )
                    # Check if there are enough tables or capacity for all diners
                    if shift.personCapacity < int(numberOfDiners):
                        return render(
                            request,
                            "reservations/reserve.html",
                            {"restaurant": restaurant, "alert": "PersonFull"},
                        )
                    # Save Reservation
                    reservationToSave = Reservation(
                        client=request.user,
                        restaurant=restaurant,
                        numberOfDiners=int(numberOfDiners),
                        shift=shift,
                        time=mydatetime,
                    )
                    reservationToSave.save()
                    # Send confirmation email
                    send_mail(
                        f"{restaurant.name} Reservation",
                        f"Your reservation for {restaurant.name} at {parse_datetime} was succesfully booked",
                        "jimypRestaurants@gmail.com",
                        [f"{request.user.email}"],
                        fail_silently=False,
                    )
                    break
            # If reservation can be booked succesfully return the restaurant page with a success alert
            return render(
                request, "reservations/index.html", {"alert": "Reservation success"}
            )
        else:
            # If restaurant is closed return to reserve page with an alert
            return render(
                request,
                "reservations/reserve.html",
                {"restaurant": restaurant, "alert": "Closed"},
            )

#API call method to get all reservations
def getReservations(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)
    reservations = request.user.reservations.all()
    serialized = []
    #For every reservation make the time timezone aware
    for reservation in reservations:
        reservation_time = timezone.localtime(reservation.time).time()
        current_time = timezone.localtime(timezone.now()).time()
        #Check if it already passed to mark as inactive
        if reservation_time < current_time:
            #Deactivate method restore shift capacities and mark them as inactive
            reservation.deactivate()
        serialized.append(reservation.serialize())

    return JsonResponse(serialized, safe=False)

#API call method to get all restaurants
def getAllRestaurants(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)
    restaurants = Restaurant.objects.all()
    return JsonResponse(
        [restaurant.serialize() for restaurant in restaurants], safe=False
    )

#API call method to cancel a reservation
def cancel(request):
    #Get the desired reservation
    data = json.loads(request.body)
    reservation_id = data.get("id")
    reservation_to_delete = Reservation.objects.get(id=reservation_id)
    #Restore the table and person capacities to the designated shift
    reservation_to_delete.shift.tablesCapacity += math.ceil(
        reservation_to_delete.numberOfDiners / 4
    )
    reservation_to_delete.shift.personCapacity += math.ceil(
        reservation_to_delete.numberOfDiners
    )
    #Save the shift capacities and delete the reservation
    reservation_to_delete.shift.save()
    reservation_to_delete.delete()
    return JsonResponse({"message": "Reservation succesfully deleted"}, status=200)

#API call to unarchive an inactive reservation (delete it)
def unarchive(request):
    #Get the desired reservation (There is no need to restore shift capacities since its done when they deactivate)
    data = json.loads(request.body)
    reservation_id = data.get("id")
    reservation_to_delete = Reservation.objects.get(id=reservation_id)
    reservation_to_delete.delete()
    return JsonResponse({"message": "Reservation succesfully unarchived"}, status=200)
    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("Home"))
        else:
            return render(
                request,
                "reservations/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "reservations/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("Home"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request,
                "reservations/register.html",
                {"message": "Passwords must match."},
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "reservations/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("Home"))
    else:
        return render(request, "reservations/register.html")
