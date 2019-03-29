from django.shortcuts import render, redirect

# Create your views here.
#https://docs.djangoproject.com/en/2.1/intro/tutorial03/

from django.http import HttpResponse
from django.template import loader
from .models import Person, Organization, Car

def home(request):
    return render(request, "home.html")

def carfinder(request):
    return render(request, "carfinder.html")

def submission(request):
    print("form submitted -- debug")

#theoretically correct but I'm not sure

    p_name = request.POST["inputName"]
    p_phone = request.POST["inputPhone"]
    p_team = request.POST["inputTeam"]

    person = Person(p_name = p_name, phone = p_phone, team = p_team)
    person.save()

    o_name = request.POST["inputOrg"]

    org = Organization(org_name = o_name)
    org.save()

    return render(request, "carfinder.html")