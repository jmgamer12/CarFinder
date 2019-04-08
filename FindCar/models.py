from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.


class Person(models.Model):
    org = models.ForeignKey('Organization', on_delete=models.CASCADE)
    p_name = models.CharField("Person's Name", max_length=45, default="")
    phone = models.PositiveIntegerField("Phone Number")
    team = models.CharField("SubTeam", max_length=45, default="")
    departTime = models.CharField(verbose_name="DepartTime", max_length=9, default="")
    #PID = models.ForeignKey('Driver', verbose_name="PersonID", primary_key=True, on_delete=models.CASCADE, unique=True)



class Event(models.Model):
    time = models.DateTimeField()
    location = models.CharField("Location", max_length=45, default="")
    org_name = models.CharField("Organization Name", max_length=45, default="Track")
    ev_name = models.CharField("Event Name", max_length=45)
    #EID = models.ForeignKey('Person', verbose_name="EventID", primary_key=True, unique=True, on_delete=models.CASCADE)



class Car(models.Model):
    numSeats = models.PositiveIntegerField("#Seats")
    timeDepart = models.DateTimeField()
    #CID = models.ForeignKey('Driver', verbose_name="CarID", primary_key=True, on_delete=models.CASCADE, unique=True)


class Driver(models.Model):
    PID = models.ForeignKey('Person', on_delete=models.CASCADE)
    CID = models.ForeignKey('Car', on_delete=models.CASCADE)

class Organization(models.Model):
    org_name = models.CharField("Org. Name", max_length=45, default="Track")

