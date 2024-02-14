
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

def reservations (request):
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
        # Parsing the datetime form field into a datetime field
        datetime = parse_datetime(request.POST["time"])
        numberOfDiners = request.POST["numberOfDiners"]
        # Getting the time only (Time field)
        mytime = datetime.time()
        # Converting the time into a string to be able to substring it later to compare to the shiftRange
        timestr = mytime.strftime('%H:%M')
        # Opening and closing times of all restaurants
        
        min = time(10, 0)
        max = time(22, 0)
        
        # if restaurant is open
        if min <= mytime <= max:
            
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
                    #Check if there are enough tables or capacity for all diners                    
                    if shift.personCapacity < int(numberOfDiners):
                        return render(
                            request,
                            "reservations/reserve.html",
                            {"restaurant": restaurant, "alert": "personFull"},
                        )
                    # Save Reservation
                    reservationToSave = Reservation(
                        client=request.user,
                        restaurant=restaurant,
                        numberOfDiners=int(numberOfDiners),
                        shift=shift,
                        time = datetime
                    )
                    reservationToSave.save()
                    # Send confirmation email
                    send_mail(
                        f"{restaurant.name} Reservation",
                        f"Your reservation for {restaurant.name} at {mytime} was succesfully booked",
                        "jimypRestaurants@gmail.com",
                        [f"{request.user.email}"],
                        fail_silently=False,
                    )
                    break
        #If reservation can be booked succesfully return the restaurant page with a success alert
        return render(request, "reservations/index.html", {"alert": "Reservation success"})
    
def getReservations(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)
    
    reservations = request.user.reservations.all()
    serialized = []
    for reservation in reservations:
        reservation_time = reservation.time.time()  
        current_time = timezone.now().time()

        if reservation_time < current_time:
            reservation.active = False
        serialized.append(reservation.serialize())
    
    return JsonResponse(
        serialized, safe=False
    )


def getAllRestaurants(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)
    restaurants = Restaurant.objects.all()
    return JsonResponse(
        [restaurant.serialize() for restaurant in restaurants], safe=False
    )
    
    
def cancel(request):
    data = json.loads(request.body)
    reservation_id = data.get("id")
    reservatio_to_delete = Reservation.objects.get(id = reservation_id)
    reservatio_to_delete.shift.tablesCapacity += math.ceil(reservatio_to_delete.numberOfDiners/4)
    reservatio_to_delete.shift.personCapacity += math.ceil(reservatio_to_delete.numberOfDiners)
    reservatio_to_delete.shift.save()
    reservatio_to_delete.delete()
    return JsonResponse(
        {"message": "Reservation succesfully deleted" }, status = 200       
    )


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
