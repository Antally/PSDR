from django.contrib import admin
from .models import Event, ShuttleBus


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'site', 'hoster', 'expected_attendees', 'start_time', 'status')
    list_filter = ('status', 'site')


@admin.register(ShuttleBus)
class ShuttleBusAdmin(admin.ModelAdmin):
    list_display = ('route', 'event', 'departure', 'capacity')