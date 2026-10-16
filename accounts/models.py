from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        DRIVER        = 'driver',        'Driver'
        EVENT_HOSTER  = 'event_hoster',  'Event Hoster'
        PARKING_OWNER = 'parking_owner', 'Parking Owner'
        ADMIN         = 'admin',         'Super Admin'

    role  = models.CharField(max_length=20, choices=Role.choices, default=Role.DRIVER)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_driver(self):        return self.role == self.Role.DRIVER
    @property
    def is_event_hoster(self):  return self.role == self.Role.EVENT_HOSTER
    @property
    def is_parking_owner(self): return self.role == self.Role.PARKING_OWNER
    @property
    def is_super_admin(self):   return self.role == self.Role.ADMIN or self.is_superuser


class DriverProfile(models.Model):
    user                  = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    default_vehicle_plate = models.CharField(max_length=20, blank=True)
    wallet_balance        = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    loyalty_points        = models.IntegerField(default=0)

    def __str__(self):
        return f"DriverProfile({self.user.username})"


class OwnerProfile(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_profile')
    company_name = models.CharField(max_length=120)
    tin_number   = models.CharField(max_length=30, blank=True)
    is_approved  = models.BooleanField(default=False)

    def __str__(self):
        return f"OwnerProfile({self.company_name})"


class EventHostProfile(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE, related_name='event_profile')
    organization = models.CharField(max_length=120)
    is_approved  = models.BooleanField(default=False)

    def __str__(self):
        return f"EventHostProfile({self.organization})"


class VehicleType(models.Model):
    """Hourly BASE price for a vehicle size. Category extra is added on top."""
    name       = models.CharField(max_length=50, unique=True)
    base_price = models.PositiveIntegerField(default=0, help_text="Base RWF per hour for this vehicle size")

    def __str__(self):
        return f"{self.name} ({self.base_price} RWF/h)"


class Vehicle(models.Model):
    driver       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.PROTECT, related_name='vehicles')
    plate_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.plate_number} ({self.vehicle_type.name})"