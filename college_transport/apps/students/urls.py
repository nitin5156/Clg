from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='student_dashboard'),
    path('buses/', views.BusListView.as_view(), name='bus_list'),
    path('booking/<int:bus_id>/', views.booking, name='booking'),
    path('create-profile/', views.create_student_profile, name='create_student_profile'),
    path('book-bus/', views.book_bus, name='book_bus'),  # New URL for booking a bus


    
]
