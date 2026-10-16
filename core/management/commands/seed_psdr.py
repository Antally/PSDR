from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from accounts.models import VehicleType, DriverProfile, OwnerProfile, EventHostProfile
from parking.models import Category, ParkingSite, Slot

User = get_user_model()


VEHICLE_TYPES = [
    ("Small car (sedan / sports)",  2000),
    ("SUV",                         3500),
    ("Small truck (coaster / bus)", 6000),
    ("Heavy lorry",                10000),
]

CATEGORIES = [
    ("Economic", 0,     "Basic parking, lit area"),
    ("Business", 3000,  "Covered parking, CCTV, guard"),
    ("Premium",  10000, "VIP protection, car wash, lounge"),
]

SITES = [
    ("Amahoro Stadium Parking",    "Amahoro, Remera, Kigali"),
    ("CHIC Building Parking",      "CHIC, Kigali"),
    ("Kimironko Market Parking",   "Kimironko, Gasabo"),
    ("Kigali Convention Centre",   "KG 2 Roundabout, Kigali"),
    ("Kigali Heights Parking",     "KG 7 Ave, Kigali"),
    ("Union Trade Centre",         "KN 4 Ave, Kigali"),
    ("Mille Collines Hotel",       "KN 6 Ave, Kigali"),
    ("Radisson Blu Kigali",        "Kigali Convention Centre"),
    ("Nyarugenge District Office", "Nyarugenge, Kigali"),
    ("Kigali International Airport","Kanombe, Kigali"),
]


class Command(BaseCommand):
    help = "Seed PSDR with categories, vehicle types, sites, slots, and demo users."

    def handle(self, *args, **options):
        for name, price in VEHICLE_TYPES:
            obj, created = VehicleType.objects.update_or_create(
                name=name, defaults={'base_price': price}
            )
            self.stdout.write(f"{'Created' if created else 'Updated'} VehicleType: {obj}")

        for name, extra, services in CATEGORIES:
            obj, created = Category.objects.update_or_create(
                name=name, defaults={'extra_price': extra, 'services': services}
            )
            self.stdout.write(f"{'Created' if created else 'Updated'} Category: {obj}")

        admin, created = User.objects.get_or_create(
            username='admin',
            defaults=dict(email='admin@psdr.rw', first_name='Super', last_name='Admin',
                          role=User.Role.ADMIN, is_staff=True, is_superuser=True),
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS("Super admin: admin / admin123"))

        owner, created = User.objects.get_or_create(
            username='owner1',
            defaults=dict(email='owner@psdr.rw', first_name='Parking', last_name='Owner',
                          role=User.Role.PARKING_OWNER),
        )
        if created:
            owner.set_password('owner123')
            owner.save()
            OwnerProfile.objects.create(user=owner, company_name='Kigali Parking Ltd', is_approved=True)
            self.stdout.write(self.style.SUCCESS("Owner: owner1 / owner123"))

        driver, created = User.objects.get_or_create(
            username='driver1',
            defaults=dict(email='driver@psdr.rw', first_name='Jean', last_name='Driver',
                          role=User.Role.DRIVER),
        )
        if created:
            driver.set_password('driver123')
            driver.save()
            DriverProfile.objects.create(user=driver)
            self.stdout.write(self.style.SUCCESS("Driver: driver1 / driver123"))

        host, created = User.objects.get_or_create(
            username='hoster1',
            defaults=dict(email='hoster@psdr.rw', first_name='Event', last_name='Hoster',
                          role=User.Role.EVENT_HOSTER),
        )
        if created:
            host.set_password('hoster123')
            host.save()
            EventHostProfile.objects.create(user=host, organization='Kigali Events Co', is_approved=True)
            self.stdout.write(self.style.SUCCESS("Hoster: hoster1 / hoster123"))

        cats = list(Category.objects.all())
        for site_name, addr in SITES:
            site, _ = ParkingSite.objects.get_or_create(
                name=site_name,
                defaults=dict(owner=owner, address=addr, status=ParkingSite.Status.APPROVED),
            )
            for i in range(1, 11):
                for cat in cats:
                    Slot.objects.get_or_create(
                        site=site, slot_number=f"{cat.name[0]}{i:02d}",
                        defaults=dict(category=cat, size=Slot.Size.SMALL),
                    )
            self.stdout.write(f"Site: {site.name} — {site.slots.count()} slots")

        self.stdout.write(self.style.SUCCESS("\nSeed complete."))
        self.stdout.write("Login credentials:")
        self.stdout.write("  admin    / admin123")
        self.stdout.write("  owner1   / owner123")
        self.stdout.write("  driver1  / driver123")
        self.stdout.write("  hoster1  / hoster123")