from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django_google_maps import fields as map_fields
# Create your models here.


class Person(models.Model):
    org = models.ForeignKey('Organization', on_delete=models.CASCADE)
    p_name = models.CharField("Person's Name", max_length=45, default="")
    phone = models.PositiveIntegerField("Phone Number")
    team = models.CharField("SubTeam", max_length=45, default="")
    departTime = models.CharField(verbose_name="DepartTime", max_length=9, default="")
    isDriver = models.IntegerField("Driver Boolean", default=0)
    #PID = models.ForeignKey('Driver', verbose_name="PersonID", primary_key=True, on_delete=models.CASCADE, unique=True)


class Event(models.Model):
    time = models.DateTimeField()
    location = models.CharField("Location", max_length=45, default="")
    org_name = models.CharField("Organization Name", max_length=45, default="Track")
    ev_name = models.CharField("Event Name", max_length=45, default="")
    #EID = models.ForeignKey('Person', verbose_name="EventID", primary_key=True, unique=True, on_delete=models.CASCADE)


class Car(models.Model):
    numSeats = models.PositiveIntegerField("#Seats")
    timeDepart = models.DateTimeField()
    make = models.CharField("Car Brand", max_length=45, default="Toyota")
    year = models.CharField("Model Year", max_length=4, default="2002")
    model = models.CharField("Car Model", max_length=15, default="Camry")
    #CID = models.ForeignKey('Driver', verbose_name="CarID", primary_key=True, on_delete=models.CASCADE, unique=True)

class Rider(models.Model):
    PID = models.ForeignKey('Person', on_delete=models.CASCADE)
    preferredDriver = models.IntegerField("Preferred DriverID", default=-1)


class Driver(models.Model):
    PID = models.ForeignKey('Person', on_delete=models.CASCADE)
    CID = models.ForeignKey('Car', on_delete=models.CASCADE)


class Organization(models.Model):
    org_name = models.CharField("Org. Name", max_length=45, default="Track")


class Maps(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)

