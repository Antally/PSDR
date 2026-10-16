from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect

from .models import User, DriverProfile, OwnerProfile, EventHostProfile


def register_choice(request):
    return render(request, 'accounts/register_choice.html')


def _register_common(request, role, extra_create=None, template='accounts/register.html'):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        first    = request.POST.get('first_name', '').strip()
        last     = request.POST.get('last_name', '').strip()

        if not username or not password:
            messages.error(request, "Username and password are required.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        else:
            u = User.objects.create_user(
                username=username, email=email, password=password,
                first_name=first, last_name=last, role=role,
            )
            if extra_create:
                extra_create(u, request)
            login(request, u)
            messages.success(request, f"Welcome, {first or username}!")
            return redirect('dashboard:router')

    return render(request, template, {'role': role})


def register_driver(request):
    def extra(u, req):
        DriverProfile.objects.create(user=u, default_vehicle_plate=req.POST.get('plate', ''))
    return _register_common(request, User.Role.DRIVER, extra)


def register_owner(request):
    def extra(u, req):
        OwnerProfile.objects.create(user=u, company_name=req.POST.get('company', ''))
    return _register_common(request, User.Role.PARKING_OWNER, extra)


def register_event_host(request):
    def extra(u, req):
        EventHostProfile.objects.create(user=u, organization=req.POST.get('organization', ''))
    return _register_common(request, User.Role.EVENT_HOSTER, extra)