# core/models.py
#
# The `core` app holds only cross-cutting utilities (landing page, template tags,
# middleware). It does NOT own any database models.
#
# The Notification model lives in the `bookings` app:
#     from bookings.models import Notification