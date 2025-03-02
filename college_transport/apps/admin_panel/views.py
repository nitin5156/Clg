from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from apps.transport.models import Bus, Route
from .forms import BusForm, RouteForm

def is_admin(user):
    return user.is_authenticated and user.user_type == 'admin'

@user_passes_test(is_admin)
def dashboard(request):
    bus_count = Bus.objects.count()
    route_count = Route.objects.count()
    return render(request, 'admin_panel/dashboard.html', {'bus_count': bus_count, 'route_count': route_count})

@user_passes_test(is_admin)
def manage_buses(request):
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_buses')
    else:
        form = BusForm()
    buses = Bus.objects.all()
    return render(request, 'admin_panel/manage_buses.html', {'form': form, 'buses': buses})

@user_passes_test(is_admin)
def assign_routes(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assign_routes')
    else:
        form = RouteForm()
    routes = Route.objects.all()
    return render(request, 'admin_panel/assign_routes.html', {'form': form, 'routes': routes})

