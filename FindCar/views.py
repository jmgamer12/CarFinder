from django.shortcuts import render, redirect
from collections import OrderedDict
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

org_list = []
org_list_final = []


# Home page
def home(request):
    context = {"home_page": "active"}
    return render(request, 'home.html', context)
    #home_template = loader.get_template('home.html')
    #return HttpResponse(home_template.render())


# INSERT functionality
def insert(request):
    global org_list_final, org_list
    cursor = connection.cursor()
    cursor.execute("SELECT * from findcar_organization")


    try:
        #result_set = cursor.fetchall()
        for row in cursor.fetchall():
            orgTup = namedtuple('OrgTup', 'id org_name')
            org_i = orgTup(row[0], row[1])
            org_list.append(org_i)

        add_org_list(org_list)

        #p1 = PersonTup(result_set[0], result_set[1], result_set[2], result_set[3], result_set[4], result_set[5])
        #print(result_set)
    except my.DataError:
        print("DataError")
    except my.ProgrammingError:
        print("Exception Occured")
    except:
        print("Unknown Error")

    context = {'items': org_list_final, "insert_page": "active"}
    return render(request, 'insert.html', context)


def add_org_list(org_list):
    global org_list_final
    for i in org_list:
        print(i[1])
        org_list_final.append(i[1])
    org_list_final = list(OrderedDict.fromkeys(org_list_final))
    print(org_list_final)


def submission(request):

    cursor = connection.cursor()
    global PID, org_idd, org_list_final, org_list
    print("form submitted -- debug")
    form = None
    if request.method == 'POST':
        form = request.POST.copy()
    print("FormType", form)


    o_name = request.POST.get("org_select", '')
    o_add_name = request.POST.get("inputOrg", '')
    p_name = request.POST.get('personName')
    print("Person Name", p_name)
    p_phone = request.POST.get("inputPhone", '')
    p_team = request.POST.get("teamInput", '')

    departTime= ""
    if (o_add_name != ""):
        org_list_final.append(o_add_name)
        cursor.execute(
            "INSERT INTO findcar_organization (org_name) VALUES ('{}')".format(
                o_add_name))

    else:
        cursor.execute(
            "INSERT INTO findcar_organization (org_name) VALUES ('{}')".format(
                o_name))
    connection.commit()
    #person = Person(p_name=p_name, phone=p_phone, team=p_team)

    cursor.execute("INSERT INTO findcar_person (p_name, phone, team, departTime, isDriver, org_id) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(p_name, p_phone, p_team, departTime, 0, org_idd))
    connection.commit()
    #person.save()

    refill_org_list(org_list_final)
    context = {"insert_page": "active", 'items': org_list_final}
    return render(request, 'insert.html', context)


def refill_org_list(org_list_final):
    cursor = connection.cursor()
    cursor.execute("SELECT * from findcar_organization")
    org_list_temp = []
    for row in cursor.fetchall():
        orgTup = namedtuple('OrgTup', 'id org_name')
        org_i = orgTup(row[0], row[1])
        org_list_temp.append(org_i)
    add_org_list(org_list_temp)


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
    query_input = request.POST.get('inputName')
    search_by = request.POST.get('query_select')
    person_list=[]
    print("Search By", search_by)
    print("Query Input", query_input)
    if(search_by=="Person"):
        cursor.execute("SELECT * FROM findcar_person WHERE p_name='{}'".format(query_input))
    elif(search_by=="Team"):
        cursor.execute("SELECT * FROM findcar_person WHERE team='{}'".format(query_input))
    elif(search_by=="Org"):
        cursor.execute("SELECT * FROM findcar_person, findcar_organization WHERE findcar_organization.org_name='{}' AND findcar_organization.id=findcar_person.org_id;".format(query_input))
    try:
        for result_set in cursor.fetchall():
            PersonTup = namedtuple('PersonTup', 'id p_name phone team departTime org_id')
            person_i = PersonTup(result_set[0], result_set[1], result_set[2], result_set[3], result_set[4], result_set[5])
            person_list.append(person_i)
        context = {'objects': person_list, "search_page": "active"}
        print(result_set)

    except my.DataError:
        print("DataError")
    except my.ProgrammingError:
        print("Exception Occured")
    except:
        print("Unknown Error")
        return render(request, 'search.html')

    return render(request, 'search.html', context)


def match(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM findcar_person;")

    try:
        result_set = cursor.fetchall()
        p1 = []

        PersonTup = namedtuple('PersonTup', 'id p_name phone team departTime org_id')
        for x in result_set:
            temp_person = PersonTup(x[0], x[1], x[2], x[3], x[4], x[5])
            p1.append(temp_person)

        context = {"match_page": "active", "people": p1}

    except my.DataError:
        print("DataError")
        return render(request, 'match.html')
    except my.ProgrammingError:
        print("Exception Occured")
        return render(request, 'match.html')
    except:
        print("Unknown Error")
        return render(request, 'match.html')

    return render(request, 'match.html', context)
