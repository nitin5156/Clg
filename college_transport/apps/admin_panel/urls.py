from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='admin_dashboard'),
    path('add-driver/', views.add_driver, name='add_driver'),  # New URL for adding a driver

    path('manage-buses/', views.manage_buses, name='manage_buses'),
    path('assign-routes/', views.assign_routes, name='assign_routes'),
    path('manage-service-records/', views.manage_service_records, name='manage_service_records'),  # New URL for managing service records

]
