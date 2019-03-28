from django.shortcuts import render

# Create your views here.
#https://docs.djangoproject.com/en/2.1/intro/tutorial03/

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")