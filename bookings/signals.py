from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Booking, Payment, PlateScanLog, Notification
from parking.models import Slot


@receiver(post_save, sender=Payment)
def payment_paid(sender, instance, created, **kwargs):
    """When a payment flips to PAID, confirm the booking and reserve the slot."""
    if instance.status == Payment.Status.PAID:
        booking = instance.booking
        if booking.status == Booking.Status.PENDING:
            booking.status = Booking.Status.CONFIRMED
            booking.save(update_fields=['status'])
            booking.slot.status = Slot.Status.RESERVED
            booking.slot.save(update_fields=['status'])
            Notification.objects.create(
                user=booking.driver,
                booking=booking,
                type=Notification.Type.PAYMENT,
                message=f"Payment received. Booking #{booking.pk} confirmed for slot {booking.slot.slot_number}.",
                link="/dashboard/driver/",
            )


@receiver(post_save, sender=PlateScanLog)
def plate_scan_handler(sender, instance, created, **kwargs):
    """Entry scan → ACTIVE + OCCUPIED. Exit scan → COMPLETED + FREE."""
    if not created:
        return
    booking = instance.booking

    if instance.event == PlateScanLog.Event.ENTRY and instance.matched:
        booking.status = Booking.Status.ACTIVE
        booking.actual_entry_time = timezone.now()
        booking.scanned_plate = instance.plate
        booking.plate_match = True
        booking.save(update_fields=['status', 'actual_entry_time', 'scanned_plate', 'plate_match'])
        booking.slot.status = Slot.Status.OCCUPIED
        booking.slot.save(update_fields=['status'])

    elif instance.event == PlateScanLog.Event.EXIT and instance.matched:
        booking.status = Booking.Status.COMPLETED
        booking.actual_exit_time = timezone.now()
        booking.save(update_fields=['status', 'actual_exit_time'])
        booking.slot.status = Slot.Status.FREE
        booking.slot.save(update_fields=['status'])


@receiver(post_save, sender=Booking)
def booking_completed_frees_slot(sender, instance, **kwargs):
    """Safety net: any COMPLETED/CANCELLED booking frees its slot."""
    if instance.status in (Booking.Status.COMPLETED, Booking.Status.CANCELLED):
        slot = instance.slot
        if slot.status != Slot.Status.FREE:
            slot.status = Slot.Status.FREE
            slot.save(update_fields=['status'])