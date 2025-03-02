from django.urls import path
from . import views

urlpatterns = [
    path('bus/<int:bus_id>/', views.bus_detail, name='bus_detail'),
    path('routes/', views.route_list, name='route_list'),
    path('booking-success/<int:booking_id>/', views.booking_success, name='booking_success'),
]

