"""
Central pricing and business logic for bookings.
Keep all money math here so views and API never duplicate it.
"""
import math
from datetime import timedelta


def booking_hours(entry_time, exit_time):
    """Minimum 1 hour, then rounded up."""
    seconds = (exit_time - entry_time).total_seconds()
    return max(1, math.ceil(seconds / 3600))


def hourly_rate(vehicle_type, category, override_price=None):
    """
    hourly = vehicle.base_price + category.extra_price
    If a PricingRule override exists (owner set a custom price), use that.
    """
    if override_price:
        return override_price
    return vehicle_type.base_price + category.extra_price


def quote(vehicle_type, category, entry_time, exit_time, override_price=None):
    """
    Return dict with hours, rate, total, and applied promo bonus.
    """
    from core.promos import compute_promo_bonus

    hours = booking_hours(entry_time, exit_time)
    rate  = hourly_rate(vehicle_type, category, override_price)
    total = hours * rate

    bonus = compute_promo_bonus(hours, category.name)

    return {
        'hours':          hours,
        'rate':           rate,
        'subtotal':       total,
        'total':          total,
        'free_minutes':   bonus['free_minutes'],
        'free_wash':      bonus['free_wash'],
        'promo_label':    bonus['label'],
    }

def extension_quote(vehicle_type, category, extra_minutes, override_price=None):
    """Cost to extend a booking by N minutes."""
    extra_hours = max(1, math.ceil(extra_minutes / 60))
    rate = hourly_rate(vehicle_type, category, override_price)
    return {
        'extra_hours': extra_hours,
        'rate':        rate,
        'extra_amount': extra_hours * rate,
    }


def overlapping_bookings(slot, entry_time, exit_time, exclude_booking_id=None):
    """Return queryset of bookings that clash with the given window."""
    from .models import Booking
    qs = Booking.objects.filter(
        slot=slot,
        status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED, Booking.Status.ACTIVE],
        entry_time__lt=exit_time,
        exit_time__gt=entry_time,
    )
    if exclude_booking_id:
        qs = qs.exclude(pk=exclude_booking_id)
    return qs