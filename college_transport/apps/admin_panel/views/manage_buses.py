from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.transport.models import Bus  # Assuming you have a Bus model
from .forms import BusForm  # Assuming you have a form for managing buses

@login_required
def manage_buses(request):
    buses = Bus.objects.all()
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new or updated bus
            return redirect('admin_dashboard')  # Redirect to admin dashboard after managing
    else:
        form = BusForm()
    return render(request, 'admin_panel/manage_buses.html', {'form': form, 'buses': buses})
