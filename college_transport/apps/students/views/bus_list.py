from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.transport.models import Bus

@login_required
def bus_list(request):
    buses = Bus.objects.all()
    return render(request, 'students/bus_list.html', {'buses': buses})
