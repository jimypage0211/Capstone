from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
import math

# User default class
class User(AbstractUser):    
    pass

# This is the shift strings from where the shft ranges will be created
shiftsArray = [
    "10:00 - 12:00",
    "12:00 - 14:00",
    "14:00 - 16:00",
    "16:00 - 18:00",
    "18:00 - 20:00",
    "20:00 - 22:00",
    "22:00 - 24:00"
]

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address =  models.CharField(max_length=255)
    img_URL = models.CharField(max_length=1000)
    personCapacity = models.IntegerField()
    tablesCapacity = models.IntegerField()

    def __str__(self):
        return self.name   
    
    # Every time a restaurant is created, all the shifts for the restaurant are automatically created
    def save (self, *args, **kwargs):
        super(Restaurant,self).save(*args, **kwargs)
        # Create shift using the shit ranges array
        for shift in shiftsArray:
            shiftToSave = Shift(
                shiftRange = shift,
                restaurant = self
            )
            shiftToSave.save()

    # Serialize method to send the model info to JS
    def serialize (self):        
        reservations = self.reservations.all()        
        reservations_Ids = []        
        for reservation in reservations:
            reservations_Ids.append(reservation.id)
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "img_URL": self.img_URL,
            "personCapacity": self.personCapacity,
            "tablesCapacity": self.tablesCapacity,
            "reservations_Ids": reservations_Ids,
        }
        
        
class Shift (models.Model):    
    shiftRange = models.CharField(max_length=14)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name= "shifts")   
    # Capacities are by default set to -1 to differentiate the creation from the edition 
    personCapacity = models.IntegerField(default = -1)
    tablesCapacity = models.IntegerField(default = -1)
    isFull = models.BooleanField(default = False, editable = False)
    
    
    def __str__(self):
        return f"{self.restaurant} - {self.shiftRange}"
    
    def save (self, *args, **kwargs):
        # When we save the shift we make sure its a new shift to assing capacities from restaurant
        if self.personCapacity == -1:
            self.personCapacity = self.restaurant.personCapacity
            self.tablesCapacity = self.restaurant.tablesCapacity    
        # If not means we are editing the shift and not creating it
        super(Shift,self).save(*args, **kwargs)
    
    # Serialize method to send the model info to JS
    def serialize (self):
        return {
            "shiftRange": self.shiftRange,
            "restaurant": self.restaurant,
            "perssonCpacity": self.personCapacity,
            "tableCapacity": self.tablesCapacity,
            "isFull": self.isFull
        }

class Reservation(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "reservations")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name = "reservations")
    numberOfDiners = models.IntegerField()
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name = "reservations")
    time = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default = True)
    
    # When we save a reservation we adjust the table and person capacities to the respective shift
    def save (self, *args, **kwargs):
        shiftToReserve = Shift.objects.get(id = self.shift.id)
        shiftToReserve.personCapacity = shiftToReserve.personCapacity - self.numberOfDiners
        # We assume all restaurant tables are for 4 person
        shiftToReserve.tablesCapacity = shiftToReserve.tablesCapacity - math.ceil(self.numberOfDiners/4)
        # If there is no more room in the shift set the shift to full
        if shiftToReserve.tablesCapacity == 0:
            shiftToReserve.isFull = True
        shiftToReserve.save()
        super(Reservation,self).save(*args, **kwargs)        
        

    def __str__(self):
        return f"{self.client.username} - {self.restaurant.name}"
    
    # This method is used for when the reservation time expires it deaactivate it
    def deactivate (self):
        # Restore the shift reservation to their previos caps
        self.shift.tablesCapacity += math.ceil(
            self.numberOfDiners / 4
        )
        self.shift.personCapacity += math.ceil(
            self.numberOfDiners
        )
        self.shift.save()
        self.active = False

    def serialize (self):
        return {
            "id": self.id,
            "restaurant_name": self.restaurant.name,
            "numberOfDiners": self.numberOfDiners,
            "shift": self.shift.shiftRange,
            "time": timezone.localtime(self.time).strftime("%b %d, %Y, %I:%M %p"),
            "active": self.active,
            "timestamp": timezone.localtime(self.timestamp).strftime("%b %d %Y, %I:%M %p"),
        }

