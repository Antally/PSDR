from django.contrib import admin
from .models import Booking, Payment, BookingExtension, PlateScanLog, Notification


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display    = ('id', 'driver', 'vehicle', 'slot',
                       'entry_time', 'exit_time', 'total_price', 'status')
    list_filter     = ('status', 'slot__site')
    search_fields   = ('vehicle__plate_number', 'driver__username')
    readonly_fields = ('total_price',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'method', 'amount', 'status', 'reference', 'approved_by_owner')
    list_filter  = ('method', 'status', 'approved_by_owner')


@admin.register(BookingExtension)
class BookingExtensionAdmin(admin.ModelAdmin):
    list_display = ('booking', 'extra_minutes', 'extra_amount', 'created_at')


@admin.register(PlateScanLog)
class PlateScanLogAdmin(admin.ModelAdmin):
    list_display = ('booking', 'event', 'plate', 'matched', 'scanned_by', 'scanned_at')
    list_filter  = ('event', 'matched')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'message', 'is_read', 'is_sent', 'created_at')
    list_filter  = ('type', 'is_read', 'is_sent')