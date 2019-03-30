from django.shortcuts import render, redirect

# Create your views here.
#https://docs.djangoproject.com/en/2.1/intro/tutorial03/

from django.http import HttpResponse
from django.template import loader
from .models import Person, Organization, Car

PID = 1000
org_id = 1
EID = 100
CID = 1

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def home(request):
    home_template = loader.get_template('home.html')
    return HttpResponse(home_template.render())


def carfinder(request):
    return render(request, 'carfinder.html')


def submission(request):
    global PID, org_id
    print("form submitted -- debug")
    o_name = request.POST.get("inputOrg")
    org = Organization(org_id=org_id, org_name=o_name)
    org_id += 1
    org.save()

    p_name = request.POST.get("inputName")
    print(p_name)
    p_phone = request.POST.get("inputPhone")
    p_team = request.POST.get("inputTeam")
    person = Person(p_name=p_name, phone=p_phone, team=p_team, org_id=org_id)
    person.save()





    return render(request, 'carfinder.html')
