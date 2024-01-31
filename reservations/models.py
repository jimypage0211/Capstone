from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):    
    pass
        
shiftsArray = [
    "10AM - 12PM",
    "12PM - 2PM",
    "2PM - 4PM",
    "4PM - 6PM",
    "6PM - 8PM",
    "8PM - 10PM",
    "10PM - 12AM"
]
        
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    personCapacity = models.IntegerField(null = False)
    tablesCapacity = models.IntegerField(null = False)

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
        shifts = self.shifts.all()
        shiftsIDS = []
        for shift in shifts:
            shiftsIDS.append(shift.id)
        return {
            "name": self.name,
            "personCapacity": self.personCapacity,
            "tablesCapacity": self.tablesCapacity,
            "isFull": self.isFull,
            "shiftsIDS": shiftsIDS
        }
        
        
class Shift (models.Model):    
    shiftRange = models.CharField(max_length=11)
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

class Reservation(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "reservations")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name = "reservations")
    numberOfDiners = models.IntegerField()
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name = "reservations")
    
    def save (self, *args, **kwargs):
        shiftToReserve = Shift.objects.get(id = self.shift.id)
        shiftToReserve.tablesCapacity = shiftToReserve.tablesCapacity -1
        shiftToReserve.personCapacity = shiftToReserve.personCapacity - self.numberOfDiners
        if shiftToReserve.tablesCapacity == 0:
            shiftToReserve.isFull = True
        shiftToReserve.save()
        super(Reservation,self).save(*args, **kwargs)        
        

    def __str__(self):
        return f"{self.client.email} - {self.restaurant.name}"

    def serialize (self):
        return {
            "client": self.client,
            "restaurant": self.restaurant,
            "numberOfDiners": self.numberOfDiners,
            "shift": self.shift.shiftRange
        }


