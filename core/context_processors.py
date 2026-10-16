from django.utils import timezone
from .promos import PROMOS


def site_globals(request):
    return {
        'SITE_NAME':    'PSDR',
        'SITE_FULL':    'Smart Parking Space Detection & Reservation',
        'SITE_TAGLINE': 'Find. Book. Park. Without the stress.',
        'SITE_CITY':    'Kigali, Rwanda',
        'SITE_EMAIL':   'YOUR_EMAIL@gmail.com',
        'SITE_PHONE':   '+250 788 123 456',
        'CURRENT_YEAR': timezone.now().year,
        'promos':       PROMOS,
    }