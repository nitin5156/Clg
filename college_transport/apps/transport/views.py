from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Bus, Route, Booking

@login_required
def bus_detail(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    return render(request, 'transport/bus_detail.html', {'bus': bus})

@login_required
def route_list(request):
    routes = Route.objects.all()
    return render(request, 'transport/route_list.html', {'routes': routes})

@login_required
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'transport/booking_success.html', {'booking': booking})

