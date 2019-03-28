from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.


class Person(models.Model):
    PID = models.ForeignKey('Driver', verbose_name="PersonID", primary_key=True, on_delete=models.CASCADE, unique=True)
    p_name = models.CharField("Person's Name", max_length=45)
    phone = models.PositiveIntegerField("Phone Number", max_length=9)
    team = models.CharField("SubTeam", max_length=45)
    departTime = models.CharField(verbose_name="DepartTime", max_length=9)


class Event(models.Model):
    EID = models.ForeignKey('Person', verbose_name="EventID", primary_key=True, unique=True, on_delete=models.CASCADE)
    time = models.DateTimeField()
    location = models.CharField("Location", max_length=45)


class Car(models.Model):
    CID = models.ForeignKey('Driver', verbose_name="CarID", primary_key=True, on_delete=models.CASCADE, unique=True)
    numSeats = models.PositiveIntegerField("#Seats")
    timeDepart = models.DateTimeField()

class Driver(models.Model):
    pass

class Organization(models.Model):
    org_name = models.ForeignKey(Person, verbose_name="Name", on_delete=models.CASCADE)