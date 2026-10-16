from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('',         views.router,           name='router'),
    path('driver/',  views.driver_dashboard, name='driver'),
    path('owner/',   views.owner_dashboard,  name='owner'),
    path('event/',   views.event_dashboard,  name='event'),
    path('admin/',   views.admin_dashboard,  name='admin'),
]