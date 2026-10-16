from django.shortcuts import render

from parking.models import ParkingSite, Slot, Category
from accounts.models import User
from bookings.models import Booking


def home(request):
    from parking.models import ParkingSite, Slot
    from accounts.models import User
    from bookings.models import Booking
    from parking.models import Review, Category
    from django.contrib import messages
    from django.shortcuts import redirect

    # Handle review submission (public — anyone logged in can review)
    if request.method == 'POST' and request.user.is_authenticated:
        rating  = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()
        if rating and rating.isdigit() and 1 <= int(rating) <= 5:
            Review.objects.create(
                driver=request.user,
                rating=int(rating),
                comment=comment,
            )
            messages.success(request, "Thanks for your review!")
            return redirect('core:home')

    # ... your existing stats/categories/steps/vehicle_rows/faqs ...
    stats = {
        'sites':    ParkingSite.objects.filter(status=ParkingSite.Status.APPROVED).count(),
        'slots':    Slot.objects.count(),
        'free':     Slot.objects.filter(status=Slot.Status.FREE).count(),
        'drivers':  User.objects.filter(role=User.Role.DRIVER).count(),
        'bookings': Booking.objects.count(),
    }

    categories = [
        {'key': 'economic', 'name': 'Economic', 'icon': 'bi-shield-check',
         'price': 2000, 'tagline': 'Smart, affordable parking',
         'features': ['Basic lighting & CCTV', 'Standard guard', 'Free entry/exit scan', 'Instant booking']},
        {'key': 'business', 'name': 'Business', 'icon': 'bi-briefcase-fill',
         'price': 5000, 'tagline': 'For busy professionals',
         'features': ['Covered & guarded slots', 'Priority lanes', 'Reserved categories', 'Business hours support']},
        {'key': 'premium', 'name': 'Premium', 'icon': 'bi-gem',
         'price': 12000, 'tagline': 'VIP treatment, every time',
         'features': ['VIP protection', 'Basic car wash included', 'Lounge access', 'Extended slots (SUVs & lorries)']},
    ]

    steps = [
        {'n': 1, 'title': 'Find the nearest parking', 'text': 'We use live location to show the closest approved PSDR site.', 'icon': 'bi-geo-alt'},
        {'n': 2, 'title': 'Pick a category & vehicle', 'text': 'Economic, Business or Premium — for sedans, SUVs, buses or lorries.', 'icon': 'bi-grid'},
        {'n': 3, 'title': 'Choose entry & exit time',  'text': 'The price updates live as you change the hours.', 'icon': 'bi-clock'},
        {'n': 4, 'title': 'Confirm & pay',             'text': 'Pay with MTN MoMo or Airtel Money in one tap.', 'icon': 'bi-credit-card'},
        {'n': 5, 'title': 'Scan, park & relax',        'text': 'Plate scan at the gate; we tell you 15 min before expiry.', 'icon': 'bi-camera-video'},
    ]

    vehicle_rows = [
        {'name': 'Small car (sedan / sports)', 'base': 2000,  'icon': 'bi-car-front-fill'},
        {'name': 'SUV',                        'base': 3500,  'icon': 'bi-car-front'},
        {'name': 'Small truck (coaster / bus)','base': 6000,  'icon': 'bi-truck'},
        {'name': 'Heavy lorry',                'base': 10000, 'icon': 'bi-truck-front-fill'},
    ]

    # Live reviews feed — newest first, top 8
    live_reviews = Review.objects.filter(is_approved=True).order_by('-created_at')[:8]

    faqs = [
        {'q': 'How do I know a slot is really available?',
         'a': 'Every booking locks the slot in real time. Sensors and plate scans at the gate confirm the car that arrived matches the car that booked.'},
        {'q': 'What happens if I arrive late?',
         'a': 'Your slot stays reserved until your booked entry window ends.'},
        {'q': 'Can I extend my stay?',
         'a': 'Yes. On your dashboard, tap "Extend Time" and pick additional minutes. You also get a 15-minute reminder before expiry.'},
        {'q': 'Which payment methods do you support?',
         'a': 'MTN MoMo and Airtel Money now. Card and cash coming soon.'},
        {'q': 'How much does it cost?',
         'a': 'Small car from 2,000 RWF/hour, SUV from 3,500, small truck from 6,000, heavy lorry from 10,000. Category add-ons apply.'},
        {'q': 'What if the plate scan fails?',
         'a': 'The owner or guard can enter the plate manually on the Scan Console.'},
    ]

    return render(request, 'core/home.html', {
        'stats':         stats,
        'categories':    categories,
        'steps':         steps,
        'vehicle_rows':  vehicle_rows,
        'live_reviews':  live_reviews,
        'faqs':          faqs,
    })
def about(request):
    return render(request, 'core/about.html')


def pricing(request):
    return render(request, 'core/pricing.html')


def terms(request):
    return render(request, 'core/terms.html')


def contact(request):
    return render(request, 'core/contact.html')