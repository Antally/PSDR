"""
Custom decorator: instead of redirecting anonymous users to /login/,
render a friendly 'create an account to continue' teaser page.
"""
from functools import wraps
from django.shortcuts import render


def login_required_page(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'core/gate.html', {
                'gate_title': 'Create a free account to continue',
                'gate_message': (
                    'You need a PSDR account to access this feature. '
                    'Sign up in 30 seconds — it is free and unlocks bookings, '
                    'dashboards, scan console, event hosting, and more.'
                ),
            })
        return view_func(request, *args, **kwargs)
    return wrapper