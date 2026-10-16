from core.decorators import login_required_page
from django.shortcuts import render


def event_list(request):
    return render(request, 'events/list.html')