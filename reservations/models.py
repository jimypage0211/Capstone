from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from django.db import models
import math


class User(AbstractUser):    
    pass
        
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
    
    def save (self, *args, **kwargs):
        super(Restaurant,self).save(*args, **kwargs)
        for shift in shiftsArray:
            shiftToSave = Shift(
                shiftRange = shift,
                restaurant = self
            )
            shiftToSave.save()

    
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
    personCapacity = models.IntegerField(default = -1)
    tablesCapacity = models.IntegerField(default = -1)
    isFull = models.BooleanField(default = False, editable = False)
    
    
    def __str__(self):
        return f"{self.restaurant} - {self.shiftRange}"
    
    def save (self, *args, **kwargs):
        if self.personCapacity == -1:
            self.personCapacity = self.restaurant.personCapacity
            self.tablesCapacity = self.restaurant.tablesCapacity    
        
        super(Shift,self).save(*args, **kwargs)
    
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
    
    def save (self, *args, **kwargs):
        shiftToReserve = Shift.objects.get(id = self.shift.id)
        shiftToReserve.personCapacity = shiftToReserve.personCapacity - self.numberOfDiners
        shiftToReserve.tablesCapacity = shiftToReserve.tablesCapacity - math.ceil(self.numberOfDiners/4)
        if shiftToReserve.tablesCapacity == 0:
            shiftToReserve.isFull = True
        shiftToReserve.save()
        super(Reservation,self).save(*args, **kwargs)        
        

    def __str__(self):
        return f"{self.client.username} - {self.restaurant.name}"
    
    def deactivate (self):
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

