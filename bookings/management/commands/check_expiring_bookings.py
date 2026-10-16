from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from bookings.models import Booking, Notification


class Command(BaseCommand):
    help = "Fire EXPIRY_SOON notifications for active bookings whose exit_time is within 15 minutes."

    def handle(self, *args, **options):
        now    = timezone.now()
        window = now + timedelta(minutes=15)

        qs = Booking.objects.filter(
            status__in=[Booking.Status.CONFIRMED, Booking.Status.ACTIVE],
            exit_time__gt=now,
            exit_time__lte=window,
        )

        count = 0
        for b in qs:
            already = Notification.objects.filter(
                booking=b,
                type=Notification.Type.EXPIRY_SOON,
                is_sent=True,
            ).exists()
            if already:
                continue

            minutes_left = max(1, int((b.exit_time - now).total_seconds() // 60))
            Notification.objects.create(
                user=b.driver,
                booking=b,
                type=Notification.Type.EXPIRY_SOON,
                message=f"Your parking ends in {minutes_left} min. Extend or pull out.",
                link="/dashboard/driver/",
                is_sent=True,
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Fired {count} expiry notifications."))