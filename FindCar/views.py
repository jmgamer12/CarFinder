from django.shortcuts import render, redirect
from collections import OrderedDict
# Create your views here.
#https://docs.djangoproject.com/en/2.1/intro/tutorial03/

from django.http import HttpResponse
import requests
import json
from django.template import loader
from .models import Person, Organization, Car
from django.db import connection, transaction
import MySQLdb as my
from collections import namedtuple
from xml.etree import ElementTree as ET

PID = 1000
org_idd = 1
EID = 100
CID = 1

org_list = []
org_list_final = []
curr_cars = dict()
num_cars = 0

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0'
}

# Home page
def get_car_list():
    global num_cars
    cursor = connection.cursor()
    cursor.execute("SELECT * from findcar_car")
    car_list = dict()
    for row in cursor.fetchall():
        key = row[5] + " " + row[3] + " " + row[4]
        mpg_seat_list = [row[1]]
        car_list[key] = mpg_seat_list
        num_cars += 1
    return car_list


def get_fegov_xml_helper(make, model, year):
    global headers
    url = "https://www.fueleconomy.gov/ws/rest/vehicle/menu/options?"
    url += "year=" + year + "&make=" + make + "&model=" + model
    response = requests.get(url, headers=headers)
    xml = ET.fromstring(response.content)
    return xml

def get_fegov_xml(car):
    global headers
    car_arr = car.split()
    url = "https://www.fueleconomy.gov/ws/rest/vehicle/menu/model?"
    year = car_arr[0]
    make = car_arr[1]
    model = car_arr[2]
    print("Model: ", model)
    url += "year=" + year + "&make=" + make
    print("List URL:", url)
    response = requests.get(url, headers=headers)
    xml = ET.fromstring(response.content)

    for item in xml.findall('menuItem'):
        val = item.find('value').text
        #print("FindAll: ", val)
        if model in val:
            print("Found: ", val)
            search_options_xml = get_fegov_xml_helper(make, val, year)
            return search_options_xml
    print("Did not Find Car")
    return None


def get_mpg(car_xml):
    global headers
    car_id = car_xml.find('menuItem').find('value').text
    url = "https://www.fueleconomy.gov/ws/rest/vehicle/" + car_id
    response = requests.get(url, headers=headers)
    new_xml = ET.fromstring(response.content)

    mpg = new_xml.find('comb08').text

    return mpg


def home(request):
    global curr_cars, num_cars
    #response = requests.get(url)

    if num_cars == len(curr_cars) and num_cars != 0:
        context = {'car_data': curr_cars, "home_page": "active"}
        return render(request, 'home.html', context)

    curr_cars = get_car_list()
    print(curr_cars)

    for car, seats in curr_cars.items():
        fegov_xml = get_fegov_xml(car)
        mpg = get_mpg(fegov_xml)
        seats.append(mpg)

    print("Car List:", curr_cars)
    events_home = getEvents()
    context = {'car_data': curr_cars, "home_page": "active", 'events': events_home}
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

        #cursor.execute("SELECT * FROM Driver NATURAL JOIN Person")

        #p1 = PersonTup(result_set[0], result_set[1], result_set[2], result_set[3], result_set[4], result_set[5])
        #print(result_set)
    except my.DataError:
        print("DataError")
    except my.ProgrammingError:
        print("Exception Occured")
    except:
        print("Unknown Error")

    drivers = getDrivers()
    events = getEvents()
    context = {'items': org_list_final, "insert_page": "active", 'drivers': drivers, 'events':   events}
    return render(request, 'insert.html', context)


def add_org_list(org_list):
    global org_list_final
    for i in org_list:
       # print(i[1])
        org_list_final.append(i[1])
    org_list_final = list(OrderedDict.fromkeys(org_list_final))
    #print(org_list_final)
   # print(org_list_final)


def get_org_id(org_name):
     cursor = connection.cursor()
     cursor.execute("SELECT * from findcar_organization WHERE org_name='{}'".format(org_name))
     result_id = cursor.fetchone()[0]
     return result_id


def check_dup(org_name):
    cursor = connection.cursor()
    cursor.execute("SELECT org_name from findcar_organization WHERE org_name='{}'".format(org_name))
    result_name = cursor.fetchone()
    print("RESULT NAME: ", result_name)
    if result_name is not None:
        return 1
    else:
        return 0


def submission(request):

    cursor = connection.cursor()
    global PID, org_idd, org_list_final, org_list
    #print("form submitted -- debug")
    form = None
    if request.method == 'POST':
        form = request.POST.copy()
    #print("FormType", form)


    o_name = request.POST.get("org_select", '')
    o_add_name = request.POST.get("inputOrg", '')
    p_name = request.POST.get('personName')
    #print("Person Name", p_name)
    p_phone = request.POST.get("inputPhone", '')
    p_team = request.POST.get("teamInput", '')
    isDriver=0
    #check radio button status
    radioDR = request.POST.get('riderSelect')
    if radioDR == 'driver':
        # new driver to db
        isDriver= 1
        d_car = request.POST.get('inputCar')
        d_carspl = d_car.split(' ')
        d_numSeats = request.POST.get('inputSeats')
        cursor.execute("INSERT INTO findcar_car (numSeats, timeDepart, make, model, year) VALUES ('{}', '{}', '{}', '{}', '{}')".format(d_numSeats, '0000-00-00 00:00:00', d_carspl[1], d_carspl[2], d_carspl[0]))
        connection.commit()

    if (o_add_name != ""):
        dup = check_dup(o_add_name)
        if dup == 0:
            org_list_final.append(o_add_name)
            cursor.execute(
                "INSERT INTO findcar_organization (org_name) VALUES ('{}')".format(
                    o_add_name))
            connection.commit()
        org_idd = get_org_id(o_add_name)

    else:
        org_idd = get_org_id(o_name)
    print("ORG ID: ", org_idd)


    #person = Person(p_name=p_name, phone=p_phone, team=p_team)

    cursor.execute("INSERT INTO findcar_person (p_name, phone, team, departTime, isDriver, org_id) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(p_name, p_phone, p_team, '', isDriver, org_idd))
    connection.commit()

    #get id of inserted person
    cursor.execute("SELECT id FROM findcar_person WHERE p_name = '{}'".format(p_name))
    person_id = cursor.fetchone()[0]

    if radioDR == 'driver':
        # adds connection to driver subclass
        cursor.execute("SELECT id FROM findcar_car WHERE numSeats = '{}' AND make = '{}'".format(d_numSeats, d_carspl[1]))
        car_id = cursor.fetchone()[0]
        #print('person id = ', person_id, ' car id = ', car_id)
        cursor.execute("INSERT INTO findcar_driver (CID_id, PID_id) VALUES ('{}', '{}')".format(car_id, person_id))
    else:
        # adds connection to rider subclass
        r_prefDrive = request.POST.get('inputPref')
        r_drivername = r_prefDrive.split(" -- ")
        #print(r_drivername)
        if r_drivername[0] == "No Preference":
            r_driverid = -1
        else:
            cursor.execute("SELECT id FROM findcar_person WHERE p_name = '{}'".format(r_drivername[0]))
            r_driverid = cursor.fetchone()[0]
        cursor.execute("INSERT INTO findcar_rider (preferredDriver, PID_id) VALUES ('{}', '{}')".format(r_driverid, person_id))

    refill_org_list(org_list_final)
    events = getEvents()
    drivers = getDrivers()
    context = {"insert_page": "active", 'items': org_list_final, 'drivers': drivers, 'events': events}
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

def getDrivers():
    cursor = connection.cursor()
    cursor.execute("SELECT p.p_name, p.phone, p.team, c.numSeats, o.org_name from findcar_driver d LEFT JOIN findcar_person p ON d.PID_id = p.id LEFT JOIN findcar_car c ON d.CID_id = c.id LEFT JOIN findcar_organization o ON p.org_id = o.id;")
    drivers = cursor.fetchall()
    driTup = namedtuple('driTup', 'name')
    driver_default = driTup("No Preference")
    driver_final = [driver_default]
    for driver in drivers:
        drive_temp = "{} -- Organization: {} -- Team: {} -- Number of Seats: {}".format(driver[0], driver[4], driver[2], driver[3])
        drive_temp2 = driTup(drive_temp)
        driver_final.append(drive_temp2)
    return driver_final


# DELETE functionality --------------------------------------------------------------------------------------
def remove(request):
    context = {"remove_page" : "active"}
    return render(request, 'remove.html', context)

def remove_person(request):
    cursor = connection.cursor()
    p_name = request.POST.get('removeInput')
    #print("Person Name", p_name)
    cursor.execute("SELECT * FROM findcar_person WHERE p_name='{}'".format(p_name))
    try:
        result_set = cursor.fetchone()
        if(result_set):
            pid=result_set[0]
            isDriver=result_set[6]

            if(isDriver==1):
                cursor.execute("UPDATE findcar_rider SET preferredDriver = -1 WHERE preferredDriver='{}'".format(pid))
                cursor.execute("SELECT * FROM findcar_driver WHERE PID_id='{}'".format(pid))
                driver=cursor.fetchone()
                if(driver):
                    cid=driver[1]
                    print(driver)
                    print(cid)
                    cursor.execute("SELECT * FROM findcar_car WHERE id='{}'".format(cid))
                    car=cursor.fetchone()
                    print(car)

                    cursor.execute("DELETE FROM findcar_driver WHERE PID_id='{}'".format(pid))
                    if(car):
                        cursor.execute("DELETE FROM findcar_car WHERE id='{}'".format(cid))

            else:
                cursor.execute("SELECT * FROM findcar_rider WHERE PID_id='{}'".format(pid))
                rider=cursor.fetchone()
                if(rider):
                    print(rider)
                    cursor.execute("DELETE FROM findcar_rider WHERE PID_id='{}'".format(pid))

            cursor.execute("DELETE FROM findcar_person WHERE id='{}'".format(pid))

            # print(result_set)

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


# UPDATE functionality ---------------------------------------------------------------------------
def update(request):
    drivers = getDrivers()
    hide = "none"
    refill_org_list(org_list_final)
    context = {"update_page": "active", "drivers": drivers, "hide": hide, "orgs": org_list_final}
    return render(request, 'update.html', context)


def update_person(request):
    cursor = connection.cursor()
    PerTup = namedtuple("PerTup", "name phone team org isDriver")
    people = []
    p_name = request.POST.get('personName')
    cursor.execute("SELECT p.id, p_name, phone, team, org_name, isDriver FROM findcar_person p LEFT JOIN findcar_organization o ON p.org_id = o.id WHERE p.p_name='{}'".format(p_name))
    try:
        result_set = cursor.fetchone()
        if result_set:
            p_phone = request.POST.get("inputPhone", '')
            p_team = request.POST.get("teamInput", '')
            if p_phone == "":
                p_phone = result_set[2]
            if p_team == "":
                p_team = result_set[3]

            radioVal = request.POST.get("riderSelect")
            prevVal = result_set[5]
            if radioVal == "rider" and prevVal == 1:
                #delete car, delete relation in driver, add relation in rider
                cursor.execute("SELECT d.PID_id as pid, d.CID_id as cid FROM findcar_person p LEFT JOIN findcar_driver d ON p.id = d.PID_id LEFT JOIN findcar_car c ON d.CID_id = c.id WHERE p.id = '{}';".format(result_set[0]))
                carRelate = cursor.fetchone()
                cursor.execute("DELETE FROM findcar_driver WHERE PID_id = '{}' AND CID_id = '{}'".format(carRelate[0], carRelate[1]))
                connection.commit()
                cursor.execute("DELETE FROM findcar_car WHERE id = '{}'".format(carRelate[1]))
                connection.commit()

                #adds relation
                r_prefDrive = request.POST.get('inputPref')
                r_drivername = r_prefDrive.split(" -- ")
                if r_drivername[0] == "No Preference":
                    r_driverid = -1
                else:
                    cursor.execute("SELECT id FROM findcar_person WHERE p_name = '{}'".format(r_drivername[0]))
                    r_driverid = cursor.fetchone()[0]
                cursor.execute("INSERT INTO findcar_rider (preferredDriver, PID_id) VALUES ('{}', '{}')".format(r_driverid, result_set[0]))
            elif radioVal == "driver" and prevVal == 0:
                #delete relation in rider, add car
                cursor.execute("SELECT PID_id as pid, preferredDriver as did FROM findcar_person p LEFT JOIN findcar_rider r ON p.id = r.PID_id WHERE p.id = '{}';".format(result_set[0]))
                riderRelate = cursor.fetchone()
                cursor.execute("DELETE FROM findcar_rider WHERE PID_id = '{}' AND preferredDriver = '{}'".format(riderRelate[0], riderRelate[1]))

                d_car = request.POST.get('inputCar')
                d_carspl = d_car.split(' ')
                d_numSeats = request.POST.get('inputSeats')
                cursor.execute("INSERT INTO findcar_car (numSeats, timeDepart, make, model, year) VALUES ('{}', '{}', '{}', '{}', '{}')".format(d_numSeats, '0000-00-00 00:00:00', d_carspl[1], d_carspl[2], d_carspl[0]))

                cursor.execute("SELECT id FROM findcar_car WHERE numSeats = '{}' AND make = '{}'".format(d_numSeats, d_carspl[1]))
                car_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO findcar_driver (CID_id, PID_id) VALUES ('{}', '{}')".format(car_id, result_set[0]))

            cursor.execute("UPDATE findcar_person SET phone='{}', team='{}', isDriver='{}' WHERE p_name='{}'".format(p_phone, p_team, 0 if radioVal == "rider" else 1, p_name))
            connection.commit()

            cursor.execute("SELECT p.id, p_name, phone, team, org_name, isDriver FROM findcar_person p LEFT JOIN findcar_organization o ON p.org_id = o.id WHERE p.p_name='{}'".format(p_name))
            newperson = cursor.fetchone()

            oldPerson = PerTup(result_set[1], result_set[2], result_set[3], result_set[4], "No" if result_set[5] == 0 else "Yes")
            updatedPerson = PerTup(newperson[1], newperson[2], newperson[3], newperson[4], "No" if newperson[5] == 0 else "Yes")

            people.append(oldPerson)
            people.append(updatedPerson)
    except my.DataError:
        print("DataError")
    except my.ProgrammingError:
        print("Exception Occured")
    except:
        print("Unknown Error")

    drivers = getDrivers()
    hide = "block"
    if not people:
        noperson = PerTup("No one found :(", "", "", "", "")
        people.append(noperson)
        people.append(noperson)
    refill_org_list(org_list_final)
    context = {"update_page": "active", "drivers": drivers, "people": people, "hide": hide, "orgs": org_list_final}
    return render(request, 'update.html', context)


# SEARCH functionality ----------------------------------------------------------
def search(request):
    context = {"search_page": "active"}
    return render(request, 'search.html', context)

def search_return(request):
    cursor = connection.cursor()
    query_input = request.POST.get('inputName')
    search_by = request.POST.get('query_select')
    search=request.POST.get('query_category')
    list=[]
    output=""
    print("Search By", search_by)
    print("Query Input", query_input)
    if(search=="People"):
        if(search_by=="Name"):
            cursor.execute("SELECT * FROM findcar_person WHERE p_name='{}'".format(query_input))
        elif(search_by=="Team"):
            cursor.execute("SELECT * FROM findcar_person WHERE team='{}'".format(query_input))
        elif(search_by=="Org"):
            cursor.execute("SELECT * FROM findcar_person, findcar_organization WHERE findcar_organization.org_name='{}' AND findcar_organization.id=findcar_person.org_id;".format(query_input))
        elif(search_by=="All"):
            cursor.execute("SELECT * FROM findcar_person")

    elif(search=="Cars"):
        if(search_by=="Name"):
            cursor.execute("SELECT * FROM findcar_person P, findcar_car C, findcar_driver D WHERE P.id=D.PID_id AND C.id=D.CID_id AND P.p_name='{}'".format(query_input))
        elif(search_by=="Team"):
            cursor.execute("SELECT * FROM findcar_person P, findcar_car C, findcar_driver D WHERE P.id=D.PID_id AND C.id=D.CID_id AND P.team='{}'".format(query_input))
        elif(search_by=="Org"):
            cursor.execute("SELECT * FROM findcar_person P, findcar_car C, findcar_driver D, findcar_organization O WHERE P.id=D.PID_id AND C.id=D.CID_id AND O.org_name='{}' AND O.id=P.org_id;".format(query_input))
        elif(search_by=="All"):
            cursor.execute("SELECT * FROM findcar_person P, findcar_car C, findcar_driver D WHERE P.id=D.PID_id AND C.id=D.CID_id")
    try:

        if(search=="Cars"):
            for result_set in cursor.fetchall():
                CarTup = namedtuple('CarTup', 'p_id p_name phone team departTime org_id is_driver car_id numSeats timeDepart make model year')
                car_i = CarTup(result_set[0], result_set[1], result_set[2], result_set[3], result_set[4], result_set[5], result_set[6], result_set[7], result_set[8], result_set[9], result_set[10], result_set[11], result_set[12])
                list.append(car_i)
            output="Car"

        else:
            for result_set in cursor.fetchall():
                PersonTup = namedtuple('PersonTup', 'id p_name phone team departTime org_id is_driver')
                person_i = PersonTup(result_set[0], result_set[1], result_set[2], result_set[3], result_set[4], result_set[5], result_set[6])
                list.append(person_i)
            output="Person"

        context = {'objects': list, 'output': output, "search_page": "active"}
        print(result_set)
    except my.DataError:
        print("DataError")
    except my.ProgrammingError:
        print("Exception Occured")
    except:
        print("Unknown Error")
        return render(request, 'search.html')

    return render(request, 'search.html', context)

#matching ------------------------------------------------------------------
def match(request):
    cursor = connection.cursor()
    cursor.execute("SELECT p1.id, r.preferredDriver as driverId, p1.p_name, p1.team, p1.phone FROM findcar_rider r LEFT JOIN findcar_person p1 on r.PID_id = p1.id LEFt JOIN findcar_person p2 on p2.id = r.preferredDriver ORDER BY p2.id;")
    result_set = cursor.fetchall()
    cursor.execute("SELECT p.id, c.make, c.model, c.year, c.numSeats, p.p_name, o.org_name, p.team, p.phone FROM findcar_driver d LEFT JOIN findcar_person p on p.id = d.PID_id LEFT JOIN findcar_car c on d.CID_id = c.id LEFT JOIN findcar_organization o on p.org_id = o.id;")
    car_set = cursor.fetchall()

    try:
        p1 = []
        cars = []

        PersonTup = namedtuple('PersonTup', 'id driverId p_name team phone matched')
        for x in result_set:
            temp_person = PersonTup(x[0], x[1], x[2], x[3], x[4], 0)
            p1.append(temp_person)

        CarTup = namedtuple('CarTup', 'id make model year numSeats p_name org_name team phone remSeats')
        for x in car_set:
            temp_car = CarTup(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[4])
            cars.append(temp_car)

        allcars = []
        for x in cars:
            matchedCar = []
            matchedCar.append(x)
            allcars.append(matchedCar)

        for car in allcars:
            for person in range(len(p1)):
                if p1[person].driverId == car[0].id and car[0].remSeats > 1 and p1[person].matched == 0:
                    p1[person] = p1[person]._replace(matched=1)
                    car[0] = car[0]._replace(remSeats=car[0].remSeats - 1)
                    car.append(p1[person])

        for car in allcars:
            for person in range(len(p1)):
                if p1[person].team == car[0].team and car[0].remSeats > 1 and p1[person].matched == 0:
                    p1[person] = p1[person]._replace(matched=1)
                    car[0] = car[0]._replace(remSeats=car[0].remSeats - 1)
                    car.append(p1[person])

        for car in allcars:
            for person in range(len(p1)):
                if p1[person].matched == 0 and car[0].remSeats > 1:
                    p1[person] = p1[person]._replace(matched=1)
                    car[0] = car[0]._replace(remSeats=car[0].remSeats - 1)
                    car.append(p1[person])

        allUnmatched = []
        for person in range(len(p1)):
            if p1[person].matched == 0:
                p1[person] = p1[person]._replace(matched=1)
                allUnmatched.append(p1[person])

        if not allUnmatched:
            message = "All people are matched"
            endMessage = PersonTup("", "", message, "", "", "")
            allUnmatched.append(endMessage)

        context = {"match_page": "active", "cars": allcars, "unmatched": allUnmatched}

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

#Events ------------------------------------------------------------
def events(request):
    events = getEvents()
    context = {"events_page": "active", "events": events}
    return render(request, 'events.html', context)

def events_add(request):
    cursor = connection.cursor()

    try:

        ev_name = request.POST.get("inputEvent")
        org_name = request.POST.get("inputOrg")
        city = request.POST.get("inputCity")
        state = request.POST.get("inputState")
        date = request.POST.get("inputDate")
        time = request.POST.get("inputTime")

        datespl = date.split("/")
        timeFinal = "{}-{}-{} {}".format(datespl[2], datespl[0], datespl[1], time)

        location = "{}, {}".format(city, state)

        cursor.execute("INSERT INTO findcar_event (time, location, org_name, ev_name) VALUES ('{}', '{}', '{}', '{}');".format(timeFinal, location, org_name, ev_name))
        connection.commit()

    except my.DataError:
        print("DataError")
        return render(request, 'match.html')
    except my.ProgrammingError:
        print("Exception Occured")
        return render(request, 'match.html')
    except:
        print("Unknown Error")
        return render(request, 'match.html')

    events = getEvents()
    context = {"events_page": "active", "events": events}
    return render(request, 'events.html', context)

def getEvents():
    cursor = connection.cursor()

    events = []

    cursor.execute("SELECT * FROM findcar_event")
    event_set = cursor.fetchall()

    EventTup = namedtuple("EventTup", "id time location org_name ev_name")

    for event in event_set:
        temp_event = EventTup(event[0], event[1], event[2], event[3], event[4])
        events.append(temp_event)

    if not events:
        temp_event2 = EventTup("", "", "", "No Events Registered", "")
        events.append(temp_event2)

    return events
