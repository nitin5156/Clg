from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='driver_dashboard'),
    path('logs/', views.driver_logs, name='driver_logs'),
    path('leave-application/', views.leave_application, name='leave_application'),
]

