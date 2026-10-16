import math
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from parking.models import PricingRule


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING   = 'pending',   'Pending payment'
        CONFIRMED = 'confirmed', 'Confirmed'
        ACTIVE    = 'active',    'Car inside'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    driver            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                          related_name='bookings')
    vehicle           = models.ForeignKey('accounts.Vehicle', on_delete=models.PROTECT,
                                          related_name='bookings')
    slot              = models.ForeignKey('parking.Slot', on_delete=models.PROTECT,
                                          related_name='bookings')
    event             = models.ForeignKey('events.Event', on_delete=models.SET_NULL,
                                          null=True, blank=True, related_name='bookings')

    entry_time        = models.DateTimeField()
    exit_time         = models.DateTimeField()
    actual_entry_time = models.DateTimeField(null=True, blank=True)
    actual_exit_time  = models.DateTimeField(null=True, blank=True)

    scanned_plate     = models.CharField(max_length=20, blank=True)
    plate_match       = models.BooleanField(default=False)

    total_price = models.PositiveIntegerField(default=0)
    status      = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at  = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking #{self.pk} - {self.vehicle.plate_number} - {self.slot}"

    # ---------- pricing ----------
    def hours(self):
        seconds = (self.exit_time - self.entry_time).total_seconds()
        return max(1, math.ceil(seconds / 3600))

    def hourly_rate(self):
        """hourly = vehicle.base_price + category.extra_price (or owner override)."""
        site     = self.slot.site
        category = self.slot.category
        vehicle_base = self.vehicle.vehicle_type.base_price

        override = PricingRule.objects.filter(site=site, category=category).first()
        if override and override.price_per_hour:
            return override.price_per_hour

        return vehicle_base + category.extra_price

    def calculate_price(self):
        return self.hours() * self.hourly_rate()

    # ---------- validation ----------
    def clean(self):
        if self.entry_time and self.exit_time and self.exit_time <= self.entry_time:
            raise ValidationError("Exit time must be after entry time.")
        if self.slot_id and self.entry_time and self.exit_time:
            clash = Booking.objects.filter(
                slot=self.slot,
                status__in=[self.Status.PENDING, self.Status.CONFIRMED, self.Status.ACTIVE],
                entry_time__lt=self.exit_time,
                exit_time__gt=self.entry_time,
            ).exclude(pk=self.pk).exists()
            if clash:
                raise ValidationError("This slot is already booked for those hours.")

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_price()
        super().save(*args, **kwargs)


class BookingExtension(models.Model):
    booking       = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='extensions')
    extra_minutes = models.PositiveIntegerField()
    extra_amount  = models.PositiveIntegerField()
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"+{self.extra_minutes} min on Booking #{self.booking_id}"


class Payment(models.Model):
    class Method(models.TextChoices):
        MTN_MOMO = 'mtn_momo',    'MTN MoMo'
        AIRTEL   = 'airtel_money','Airtel Money'
        CARD     = 'card',        'Card'
        CASH     = 'cash',        'Cash'

    class Status(models.TextChoices):
        PENDING  = 'pending',  'Pending'
        PAID     = 'paid',     'Paid'
        FAILED   = 'failed',   'Failed'
        REFUNDED = 'refunded', 'Refunded'

    booking   = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    method    = models.CharField(max_length=20, choices=Method.choices)
    amount    = models.PositiveIntegerField()
    status    = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    reference = models.CharField(max_length=60, blank=True)
    paid_at   = models.DateTimeField(null=True, blank=True)
    approved_by_owner = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment #{self.booking_id}: {self.amount} RWF ({self.status})"


class PlateScanLog(models.Model):
    class Event(models.TextChoices):
        ENTRY = 'entry', 'Entry'
        EXIT  = 'exit',  'Exit'

    booking    = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='scans')
    scanned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    event      = models.CharField(max_length=10, choices=Event.choices)
    plate      = models.CharField(max_length=20)
    matched    = models.BooleanField(default=False)
    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event} {self.plate} @ {self.scanned_at:%Y-%m-%d %H:%M}"


class Notification(models.Model):
    """Lives inside bookings app (Option A)."""
    class Type(models.TextChoices):
        INFO           = 'info',           'Info'
        EXPIRY_SOON    = 'expiry_soon',    'Expiry soon (15 min)'
        EXPIRED        = 'expired',        'Expired'
        PAYMENT        = 'payment',        'Payment'
        PLATE_MISMATCH = 'plate_mismatch', 'Plate mismatch'
        EVENT          = 'event',          'Event'

    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='notifications')
    booking    = models.ForeignKey(Booking, on_delete=models.CASCADE,
                                   null=True, blank=True, related_name='notifications')
    type       = models.CharField(max_length=20, choices=Type.choices, default=Type.INFO)
    message    = models.CharField(max_length=255)
    link       = models.CharField(max_length=200, blank=True)
    is_read    = models.BooleanField(default=False)
    is_sent    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.message[:40]}"