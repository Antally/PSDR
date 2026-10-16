from django.conf import settings
from django.db import models


class Event(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        COMPLETED = 'completed', 'Completed'

    hoster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='events')
    site = models.ForeignKey('parking.ParkingSite', on_delete=models.PROTECT,
                             related_name='events')
    name = models.CharField(max_length=150)
    expected_attendees = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"{self.name} @ {self.site.name}"


class ShuttleBus(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='shuttle_buses')
    route = models.CharField(max_length=200)
    departure = models.DateTimeField()
    capacity = models.PositiveIntegerField(default=30)

    class Meta:
        verbose_name_plural = 'shuttle buses'

    def __str__(self):
        return f"{self.route} ({self.departure:%d %b %H:%M})"