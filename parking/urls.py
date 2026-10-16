from django.urls import path
from . import views

app_name = 'parking'

urlpatterns = [
    path('',                views.site_list,   name='site_list'),
    path('<int:pk>/',       views.site_detail, name='site_detail'),
    path('scan/',           views.scan_console, name='scan'),
]