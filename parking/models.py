from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Category(models.Model):
    """
    Economic, Business, Premium — extra price is added to the vehicle's base price.
    """
    name        = models.CharField(max_length=50, unique=True)
    extra_price = models.PositiveIntegerField(
        default=0,
        help_text="RWF/h added on top of vehicle base price"
    )
    services    = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class ParkingSite(models.Model):
    class Status(models.TextChoices):
        PENDING   = 'pending',   'Pending approval'
        APPROVED  = 'approved',  'Approved'
        SUSPENDED = 'suspended', 'Suspended'

    owner       = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='parking_sites'
    )
    name        = models.CharField(max_length=120)
    address     = models.CharField(max_length=255)
    latitude    = models.FloatField(null=True, blank=True)
    longitude   = models.FloatField(null=True, blank=True)
    status      = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    regulations = models.TextField(blank=True)
    offers      = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Slot(models.Model):
    class Status(models.TextChoices):
        FREE        = 'free',        'Free'
        RESERVED    = 'reserved',    'Reserved'
        OCCUPIED    = 'occupied',    'Occupied'
        MAINTENANCE = 'maintenance', 'Maintenance'

    class Size(models.TextChoices):
        SMALL  = 'small',  'Small'
        MEDIUM = 'medium', 'Medium'
        LARGE  = 'large',  'Large'

    site        = models.ForeignKey(
        ParkingSite, on_delete=models.CASCADE, related_name='slots'
    )
    category    = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='slots'
    )
    slot_number = models.CharField(max_length=20)
    size        = models.CharField(
        max_length=10, choices=Size.choices, default=Size.SMALL
    )
    status      = models.CharField(
        max_length=20, choices=Status.choices, default=Status.FREE
    )

    class Meta:
        unique_together = ('site', 'slot_number')
        ordering = ['site', 'slot_number']

    def __str__(self):
        return f"{self.site.name} - {self.slot_number} ({self.category.name})"


class PricingRule(models.Model):
    """
    Optional: lets an owner set a custom hourly price for one category at their site.
    """
    site           = models.ForeignKey(
        ParkingSite, on_delete=models.CASCADE, related_name='pricing_rules'
    )
    category       = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='pricing_rules'
    )
    price_per_hour = models.PositiveIntegerField(help_text="RWF per hour")

    class Meta:
        unique_together = ('site', 'category')

    def __str__(self):
        return f"{self.site.name} - {self.category.name}: {self.price_per_hour} RWF/h"


class Review(models.Model):
    """
    User-submitted review. Site is optional so users can review the platform itself.
    is_approved defaults to True so new reviews appear on the homepage immediately.
    """
    driver      = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    site        = models.ForeignKey(
        ParkingSite,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True
    )
    rating      = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment     = models.TextField(blank=True)
    is_approved = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('driver', 'site')

    def __str__(self):
        return f"{self.driver.username}: {self.rating}/5"