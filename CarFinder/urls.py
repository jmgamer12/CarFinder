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

    path('home/', views.home, name='home'),

    path('insert/', views.insert, name='insert'),
    path('insert_submit/', views.submission, name='insert_submit'),

    path('remove/', views.remove, name='remove'),
    path('remove_person/', views.remove_person, name='remove_person'),

    path('update/', views.update, name='update'),
    path('update_person/', views.update_person, name='update_person'),

    path('search/', views.search, name='search'),
    path('search_return/', views.search_return, name='search_return'),

    path('match/', views.match, name='match'),

    path('events/', views.events, name='events'),
    path('events_add/', views.events_add, name='events_add')
]
