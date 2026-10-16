from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (User, VehicleType, Vehicle,
                     DriverProfile, OwnerProfile, EventHostProfile)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Parking System', {'fields': ('role', 'phone')}),
    )
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter  = ('role', 'is_staff')


@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price')
    ordering     = ('base_price',)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display  = ('plate_number', 'vehicle_type', 'driver')
    list_filter   = ('vehicle_type',)
    search_fields = ('plate_number', 'driver__username')


admin.site.register(DriverProfile)
admin.site.register(OwnerProfile)
admin.site.register(EventHostProfile)