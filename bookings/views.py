from core.decorators import login_required_page
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.models import Vehicle, VehicleType
from parking.models import ParkingSite, Slot, Category, PricingRule
from .models import Booking, Payment, BookingExtension, Notification
from . import services


# ---------- WIZARD (chunk 2 will flesh this out) ----------
@login_required
def wizard(request, site_id=None):
    sites = ParkingSite.objects.filter(status=ParkingSite.Status.APPROVED)
    context = {
        'sites': sites,
        'preselected_site_id': site_id,
    }
    return render(request, 'bookings/wizard.html', context)


# ---------- API: live quote ----------
@login_required
def api_quote(request):
    """
    GET params:
      vehicle_type_id, category_id, entry, exit (ISO), site_id (optional)
    Returns JSON: { hours, rate, total }
    """
    try:
        vt_id  = int(request.GET.get('vehicle_type_id', 0))
        cat_id = int(request.GET.get('category_id', 0))
        entry  = request.GET.get('entry')
        exit_  = request.GET.get('exit')
        site_id = request.GET.get('site_id')

        vt  = VehicleType.objects.get(pk=vt_id)
        cat = Category.objects.get(pk=cat_id)
        entry_dt = timezone.datetime.fromisoformat(entry)
        exit_dt  = timezone.datetime.fromisoformat(exit_)

        if timezone.is_naive(entry_dt):
            entry_dt = timezone.make_aware(entry_dt)
        if timezone.is_naive(exit_dt):
            exit_dt = timezone.make_aware(exit_dt)

        override = None
        if site_id:
            rule = PricingRule.objects.filter(site_id=site_id, category=cat).first()
            if rule:
                override = rule.price_per_hour

        q = services.quote(vt, cat, entry_dt, exit_dt, override)
        return JsonResponse({'ok': True, **q})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)


# ---------- API: available slots ----------
@login_required
def api_slots(request):
    """
    GET params: site_id, category_id, entry, exit
    Returns list of slots not overlapping the window.
    """
    try:
        site_id = int(request.GET.get('site_id'))
        cat_id  = int(request.GET.get('category_id'))
        entry   = request.GET.get('entry')
        exit_   = request.GET.get('exit')

        entry_dt = timezone.datetime.fromisoformat(entry)
        exit_dt  = timezone.datetime.fromisoformat(exit_)
        if timezone.is_naive(entry_dt):
            entry_dt = timezone.make_aware(entry_dt)
        if timezone.is_naive(exit_dt):
            exit_dt = timezone.make_aware(exit_dt)

        slots = Slot.objects.filter(site_id=site_id, category_id=cat_id).exclude(
            status=Slot.Status.MAINTENANCE
        )

        available = []
        for s in slots:
            if not services.overlapping_bookings(s, entry_dt, exit_dt).exists():
                available.append({
                    'id': s.id,
                    'slot_number': s.slot_number,
                    'size': s.get_size_display(),
                    'status': s.get_status_display(),
                })
        return JsonResponse({'ok': True, 'slots': available})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)


# ---------- PAYMENT (chunk 3 will flesh out) ----------
@login_required
def pay(request, pk):
    booking = get_object_or_404(Booking, pk=pk, driver=request.user)
    return render(request, 'bookings/payment.html', {'booking': booking})


# ---------- RECEIPT (chunk 3) ----------
@login_required
def receipt(request, pk):
    booking = get_object_or_404(Booking, pk=pk, driver=request.user)
    return render(request, 'bookings/receipt.html', {'booking': booking})


# ---------- EXTEND (chunk 4) ----------
@login_required
@require_POST
def extend_booking(request, pk):
    messages.info(request, "Extend feature arrives in the next chunk.")
    return redirect('dashboard:driver')


# ---------- CANCEL ----------
@login_required
@require_POST
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, driver=request.user)
    if booking.status in (Booking.Status.PENDING, Booking.Status.CONFIRMED):
        booking.status = Booking.Status.CANCELLED
        booking.save()
        messages.success(request, f"Booking #{booking.pk} cancelled.")
    else:
        messages.warning(request, "This booking can no longer be cancelled.")
    return redirect('dashboard:driver')