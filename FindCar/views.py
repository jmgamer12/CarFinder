from django.shortcuts import render, redirect

# Create your views here.
#https://docs.djangoproject.com/en/2.1/intro/tutorial03/

from django.http import HttpResponse
from django.template import loader
from .models import Person, Organization, Car
from django.db import connection, transaction

PID = 1000
org_idd = 1
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
    cursor = connection.cursor()
    global PID, org_idd
    print("form submitted -- debug")
    form = None
    if request.method == 'POST':
        form = request.POST.copy()
    print("FormType", form)
    '''
    
    org = Organization(org_name=o_name)
    org_id += 1
    org.save()
    '''
    o_name = request.POST.get("orgInput")
    p_name = request.POST.get('personName')
    print("Person Name", p_name)
    p_phone = request.POST.get("inputPhone", '')
    p_team = request.POST.get("teamInput", '')
    departTime= ""

    cursor.execute(
        "INSERT INTO findcar_organization (org_name) VALUES ('{}')".format(
            o_name))
    connection.commit()
    #person = Person(p_name=p_name, phone=p_phone, team=p_team)
    cursor.execute("INSERT INTO findcar_person (p_name, phone, team, departTime, org_id) VALUES ('{}', '{}', '{}', '{}', '{}')".format(p_name, p_phone, p_team, departTime, org_idd))
    connection.commit()
    #person.save()

    return render(request, 'carfinder.html')

def remove_person(request):
    per_name = request.POST.get("removeInput")
    death = Person.objects.filter(p_name=per_name).delete()
    return render(request, 'remove_person_temp.html')
