from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DriverForm  # Assuming you have a form for adding drivers

@login_required
def add_driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new driver
            return redirect('admin_dashboard')  # Redirect to admin dashboard after adding
    else:
        form = DriverForm()
    return render(request, 'admin_panel/add_driver.html', {'form': form})
