from django.contrib import admin
from .models import Category, ParkingSite, Slot, PricingRule, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'extra_price', 'services')


@admin.register(ParkingSite)
class ParkingSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'address', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'address')


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('slot_number', 'site', 'category', 'status')
    list_filter = ('site', 'category', 'status')


@admin.register(PricingRule)
class PricingRuleAdmin(admin.ModelAdmin):
    list_display = ('site', 'category', 'price_per_hour')
    list_filter = ('site', 'category')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('site', 'driver', 'rating')
    list_filter = ('rating',)