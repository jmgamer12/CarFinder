from django.shortcuts import render, redirect

# Create your views here.
#https://docs.djangoproject.com/en/2.1/intro/tutorial03/

from django.http import HttpResponse
from django.template import loader
from .models import Person, Organization, Car
from django.db import connection, transaction
import MySQLdb as my
from collections import namedtuple

PID = 1000
org_idd = 1
EID = 100
CID = 1

# Home page
def home(request):
    context = {"home_page": "active"}
    return render(request, 'home.html', context)
    #home_template = loader.get_template('home.html')
    #return HttpResponse(home_template.render())

# INSERT functionality
def insert(request):
    context = {"insert_page": "active"}
    return render(request, 'insert.html', context)
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

    context = {"insert_page": "active"}
    return render(request, 'insert.html', context)


# DELETE functionality
def remove(request):
    context = {"remove_page" : "active"}
    return render(request, 'remove.html', context)
def remove_person(request):
    cursor = connection.cursor()
    p_name = request.POST.get('removeInput')
    print("Person Name", p_name)
    cursor.execute("SELECT * FROM findcar_person WHERE p_name='{}'".format(p_name))
    try:
        result_set = cursor.fetchone()[0]
        if result_set:
            cursor.execute("DELETE FROM findcar_person WHERE p_name='{}'".format(p_name))
    except my.DataError:
        print("DataError")
    except my.ProgrammingError:
        print("Exception Occured")
    except:
        print("Unknown Error")

    context = {"remove_page": "active"}
    return render(request, 'remove.html', context)

'''
This function is supposed to find the name given in the form and determine if it is actually present
in the table via try/except (if not in table cursor.fetchone should return a programming error)

If present then proceed to update table as the usual. Also if you could, change the remove function to
be a raw query as well
'''
# UPDATE functionality
def update(request):
    context = {"update_page" : "active"}
    return render(request, 'update.html', context)
def update_person(request):
    cursor = connection.cursor()
    p_name = request.POST.get('personName')
    print("Person Name", p_name)
    cursor.execute("SELECT * FROM findcar_person WHERE p_name='{}'".format(p_name))
    try:
        result_set = cursor.fetchone()[0]
        if (result_set):
            p_phone = request.POST.get("inputPhone", '')
            p_team = request.POST.get("teamInput", '')
            #o_name = request.POST.get("orgInput")
            cursor.execute("UPDATE findcar_person SET phone='{}', team='{}' WHERE p_name='{}'".format(p_phone, p_team, p_name))

    except my.DataError:
        print("DataError")
    except my.ProgrammingError:
        print("Exception Occured")
    except:
        print("Unknown Error")

    context = {"update_page": "active"}
    return render(request, 'update.html', context)

# SEARCH functionality
def search(request):
    context = {"search_page": "active"}
    return render(request, 'search.html', context)
def search_return(request):
    cursor = connection.cursor()
    p_name = request.POST.get('personName')
    print("Person Name", p_name)
    cursor.execute("SELECT * FROM findcar_person WHERE p_name='{}'".format(p_name))

    try:
        result_set = cursor.fetchone()

        PersonTup = namedtuple('PersonTup', 'id p_name phone team departTime org_id')
        p1 = PersonTup(result_set[0], result_set[1], result_set[2], result_set[3], result_set[4], result_set[5])

        context = {'object': p1, "search_page": "active"}
        print(result_set)

    except my.DataError:
        print("DataError")
    except my.ProgrammingError:
        print("Exception Occured")
    except:
        print("Unknown Error")

    return render(request, 'search.html', context)

