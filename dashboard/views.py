from core.decorators import login_required_page
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from bookings.models import Booking, Notification


@login_required
def router(request):
    u = request.user
    if u.is_super_admin:
        return redirect('dashboard:admin')
    if u.is_parking_owner:
        return redirect('dashboard:owner')
    if u.is_event_hoster:
        return redirect('dashboard:event')
    return redirect('dashboard:driver')


@login_required
def driver_dashboard(request):
    now = timezone.now()
    active_bookings = Booking.objects.filter(
        driver=request.user,
        status__in=[Booking.Status.CONFIRMED, Booking.Status.ACTIVE],
    ).order_by('exit_time')
    past_bookings = Booking.objects.filter(
        driver=request.user,
        status__in=[Booking.Status.COMPLETED, Booking.Status.CANCELLED],
    ).order_by('-created_at')[:10]
    unread = Notification.objects.filter(user=request.user, is_read=False).count()

    return render(request, 'dashboard/driver.html', {
        'active_bookings': active_bookings,
        'past_bookings':   past_bookings,
        'unread_count':    unread,
        'now':             now,
    })


@login_required
def owner_dashboard(request):
    return render(request, 'dashboard/owner.html')


@login_required
def event_dashboard(request):
    return render(request, 'dashboard/event.html')


@login_required
def admin_dashboard(request):
    return render(request, 'dashboard/admin.html')