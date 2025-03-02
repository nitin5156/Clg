from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from apps.transport.models import Bus, Booking
from .forms import BookingForm
from .booking import book_bus  # Correctly import the book_bus function from booking.py

from apps.accounts.models import CustomUser
from apps.students.models import Student

@login_required
def dashboard(request):
    try:
        student = request.user.student
    except AttributeError:
        return render(request, 'students/dashboard.html', {
            'bookings': [],
            'profile_missing': True
        })
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from apps.transport.models import Bus, Booking
from .forms import BookingForm
from .booking import book_bus
from apps.accounts.models import CustomUser
from apps.students.models import Student
from django.contrib import messages

@login_required
def dashboard(request):
    try:
        student = request.user.student
    except AttributeError:
        return render(request, 'students/dashboard.html', {
            'bookings': [],
            'profile_missing': True
        })

    bookings = Booking.objects.filter(student=student)
    return render(request, 'students/dashboard.html', {'bookings': bookings})

class BusListView(LoginRequiredMixin, ListView):
    model = Bus
    template_name = 'students/bus_list.html'
    context_object_name = 'buses'
    paginate_by = 10

@login_required
def booking(request, bus_id):
    bus = Bus.objects.get(id=bus_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.student = request.user.student
            booking.bus = bus
            booking.save()
            messages.success(request, 'Booking successful!')
            return redirect('booking_success', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'students/booking.html', {'form': form, 'bus': bus})

def create_student_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        
        if CustomUser.objects.filter(username=email).exists():
            messages.error(request, 'A user with this email already exists.')
            return render(request, 'students/create_profile.html')
        
        user = CustomUser.objects.create_user(username=email, email=email, password='defaultpassword')
        student = Student.objects.create(user=user, student_id=uuid.uuid4().hex[:10].upper(), department="Not Assigned")
        
        messages.success(request, 'Profile created successfully!')
        return redirect('student_dashboard')
    return render(request, 'students/create_profile.html')

@login_required
def book_bus(request):
    buses = Bus.objects.all()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.student = request.user.student
            booking.save()
            messages.success(request, 'Booking successful!')
            return redirect('booking_success', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'students/booking.html', {'form': form, 'buses': buses})

@login_required
def bus_list(request):
    buses = Bus.objects.all()
    return render(request, 'students/bus_list.html', {'buses': buses})
    bookings = Booking.objects.filter(student=student)
    return render(request, 'students/dashboard.html', {'bookings': bookings})

class BusListView(LoginRequiredMixin, ListView):
    model = Bus
    template_name = 'students/bus_list.html'
    context_object_name = 'buses'

@login_required
def booking(request, bus_id):
    bus = Bus.objects.get(id=bus_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.student = request.user.student
            booking.bus = bus
            booking.save()
            return redirect('booking_success', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'students/booking.html', {'form': form, 'bus': bus})

def create_student_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        
        if CustomUser.objects.filter(username=email).exists():
            return render(request, 'students/create_profile.html', {
                'error': 'A user with this email already exists.'
            })
        
        user = CustomUser.objects.create_user(username=email, email=email, password='defaultpassword')
        student = Student.objects.create(user=user, student_id=uuid.uuid4().hex[:10].upper(), department="Not Assigned")
        
        return redirect('student_dashboard')
    return render(request, 'students/create_profile.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.transport.models import Bus, Booking
from .forms import BookingForm

@login_required
def book_bus(request):
    buses = Bus.objects.all()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.student = request.user.student
            booking.save()
            return redirect('booking_success', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'students/booking.html', {'form': form, 'buses': buses})
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.transport.models import Bus

@login_required
def bus_list(request):
    buses = Bus.objects.all()
    return render(request, 'students/bus_list.html', {'buses': buses})
