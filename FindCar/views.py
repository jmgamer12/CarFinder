from django.shortcuts import render

# Create your views here.
#https://docs.djangoproject.com/en/2.1/intro/tutorial03/

from django.http import HttpResponse
from django.template import loader


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    home_template = loader.get_template('home.html')
    return HttpResponse(home_template.render())

def carfinder(request):
    cf_template = loader.get_template('carfinder.html')
    return HttpResponse(cf_template.render())