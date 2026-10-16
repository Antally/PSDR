from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event_list'),
]


# if `events/views.py` is empty, create this minimal version:
# from django.shortcuts import render
# def event_list(request): return render(request, 'events/list.html')