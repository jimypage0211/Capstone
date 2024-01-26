from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):    
    pass


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    personCapacity = models.IntegerField(null = False)
    tablesCapacity = models.IntegerField(null = False)
    reserverdTables = models.IntegerField()
    isFull = models.BooleanField(default = False)

    def __str__(self):
        return self.name
    
    def serialize (self):
        reservations = self.reservations.all()
        reservationsIDs = []
        for reservation in reservations:
            reservationsIDs.append(reservation.id)
        return {
            "name": self.name,
            "personCapacity": self.personCapacity,
            "maxTables": self.tablesCapacity,
            "reserverdTables": self.reserverdTables,
            "isFull": self.isFull,
            "reservationsIDs": reservationsIDs
        }

class Reservation(models.Model):
    time  = models.DateTimeField()
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "reservations")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name = "reservations")
    numberOfDiners = models.IntegerField()

    def __str__(self):
        return f"{self.client.email} - {self.time} - {self.restaurant.name}"

    def serialize (self):
        return {
            "time": self.time,
            "client": self.client,
            "restaurant": self.restaurant,
            "numberOfDiners": self.numberOfDiners
        }



