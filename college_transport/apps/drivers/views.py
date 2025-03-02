from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import DriverLog, LeaveApplication
from .forms import DriverLogForm, LeaveApplicationForm

@login_required
def dashboard(request):
    logs = DriverLog.objects.filter(driver=request.user.driver).order_by('-date')[:5]
    leave_applications = LeaveApplication.objects.filter(driver=request.user.driver).order_by('-start_date')[:5]
    return render(request, 'drivers/dashboard.html', {'logs': logs, 'leave_applications': leave_applications})

@login_required
def driver_logs(request):
    if request.method == 'POST':
        form = DriverLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.driver = request.user.driver
            log.save()
            return redirect('driver_logs')
    else:
        form = DriverLogForm()
    logs = DriverLog.objects.filter(driver=request.user.driver).order_by('-date')
    return render(request, 'drivers/logs.html', {'form': form, 'logs': logs})

@login_required
def leave_application(request):
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.driver = request.user.driver
            leave.save()
            return redirect('driver_dashboard')
    else:
        form = LeaveApplicationForm()
    return render(request, 'drivers/leave_application.html', {'form': form})

