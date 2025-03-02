from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.transport.models import Bus, Route  # Assuming you have a Route model
from .forms import AssignRouteForm  # Assuming you have a form for assigning routes

@login_required
def assign_routes(request):
    if request.method == 'POST':
        form = AssignRouteForm(request.POST)
        if form.is_valid():
            form.save()  # Save the assigned route
            return redirect('admin_dashboard')  # Redirect to admin dashboard after assignment
    else:
        form = AssignRouteForm()
    return render(request, 'admin_panel/assign_routes.html', {'form': form})
