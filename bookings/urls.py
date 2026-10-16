from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # Wizard
    path('new/',                         views.wizard,           name='wizard'),
    path('new/<int:site_id>/',           views.wizard,           name='wizard_site'),

    # API endpoints (JSON)
    path('api/quote/',                   views.api_quote,        name='api_quote'),
    path('api/slots/',                   views.api_slots,        name='api_slots'),

    # Actions
    path('<int:pk>/pay/',                views.pay,              name='pay'),
    path('<int:pk>/receipt/',            views.receipt,          name='receipt'),
    path('<int:pk>/extend/',             views.extend_booking,   name='extend'),
    path('<int:pk>/cancel/',             views.cancel_booking,   name='cancel'),
]