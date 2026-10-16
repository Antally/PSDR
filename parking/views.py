from core.decorators import login_required_page
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .models import ParkingSite, Slot


def site_list(request):
    sites = ParkingSite.objects.filter(status=ParkingSite.Status.APPROVED)
    return render(request, 'parking/site_list.html', {'sites': sites})


def site_detail(request, pk):
    site = get_object_or_404(ParkingSite, pk=pk)
    slots = site.slots.all()
    return render(request, 'parking/site_detail.html', {'site': site, 'slots': slots})


@login_required
def scan_console(request):
    """Owner scan console — chunk 5 will flesh this out."""
    return render(request, 'parking/scan.html')