"""CarFinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.urls import include, path

from django.contrib import admin

from FindCar import views

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('car_submission', views.submission, name='car_submission'),
    path('home/', views.home),
    path('carfinder.html', views.carfinder),
    path('home/carfinder/', views.carfinder),
    path('carfinder/home', views.home),
    path('carfinder', views.carfinder),
    path('carfinder/', views.carfinder),
    path('remove_person_temp.html', views.remove_person, name='remove_person')
]
