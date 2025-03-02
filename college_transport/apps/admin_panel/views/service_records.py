from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.transport.models import ServiceRecord  # Assuming you have a ServiceRecord model
from .forms import ServiceRecordForm  # Assuming you have a form for managing service records

@login_required
def manage_service_records(request):
    records = ServiceRecord.objects.all()
    if request.method == 'POST':
        form = ServiceRecordForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new or updated service record
            return redirect('admin_dashboard')  # Redirect to admin dashboard after managing
    else:
        form = ServiceRecordForm()
    return render(request, 'admin_panel/manage_service_records.html', {'form': form, 'records': records})
