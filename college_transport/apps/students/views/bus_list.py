from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.db.models import Q, Count, Case, When, IntegerField, F
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from django_ratelimit.decorators import ratelimit
from django.core.cache import cache
from django.db import transaction
from apps.transport.models import Bus, Route, Booking
from apps.students.models import Student
import logging

logger = logging.getLogger(__name__)

class BusListView(LoginRequiredMixin, UserPassesTestMixin):
    model = Bus
    template_name = 'students/bus_list.html'
    context_object_name = 'buses'
    paginate_by = 10
    raise_exception = True

    @method_decorator(csrf_protect)
    @method_decorator(cache_page(60))  # Cache the page for 1 minute
    @method_decorator(ratelimit(key='user', rate='30/m', method=['GET'], block=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def test_func(self):
        try:
            student = self.request.user.student
            return bool(student and student.is_active)
        except (AttributeError, Student.DoesNotExist):
            logger.warning(f"Unauthorized access attempt by user {self.request.user.id}")
            return False

    def get_queryset(self):
        try:
            today = timezone.now().date()
            cache_key = f'bus_list_{today.isoformat()}'
            queryset = cache.get(cache_key)
            
            if queryset is None:
                # Start with all buses and optimize queries
                queryset = Bus.objects.select_related('driver').prefetch_related(
                    'route_set',
                    'booking_set'
                ).annotate(
                    available_seats=Case(
                        When(
                            booking__date=today,
                            booking__status='confirmed',
                            then=F('capacity') - Count('booking')
                        ),
                        default=F('capacity'),
                        output_field=IntegerField(),
                    )
                ).distinct()
                
                cache.set(cache_key, queryset, 300)  # Cache for 5 minutes
            
            # Apply filters
            search_query = self.request.GET.get('search', '').strip()
            if search_query:
                # Sanitize the search query
                search_query = search_query[:100]  # Limit length
                queryset = queryset.filter(
                    Q(bus_number__icontains=search_query) |
                    Q(route__name__icontains=search_query) |
                    Q(driver__name__icontains=search_query)
                )

            available = self.request.GET.get('available')
            if available:
                queryset = queryset.filter(available_seats__gt=0)

            route = self.request.GET.get('route', '').strip()
            if route:
                route = route[:100]  # Limit length
                queryset = queryset.filter(route__name__icontains=route)

            return queryset

        except Exception as e:
            logger.error(f"Error in get_queryset: {str(e)}")
            raise ValidationError("An error occurred while fetching the bus list.")

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            
            # Sanitize and validate input parameters
            context['search_query'] = self.request.GET.get('search', '')[:100]
            context['available_filter'] = bool(self.request.GET.get('available'))
            context['route_filter'] = self.request.GET.get('route', '')[:100]
            
            # Get routes from cache or database
            cache_key = 'all_routes'
            routes = cache.get(cache_key)
            if routes is None:
                routes = list(Route.objects.values_list('name', flat=True).distinct())
                cache.set(cache_key, routes, 3600)  # Cache for 1 hour
            context['routes'] = routes
            
            # Process bus information
            buses_with_info = []
            today = timezone.now().date()
            
            for bus in context['buses']:
                with transaction.atomic():
                    # Get routes
                    routes = bus.route_set.all()
                    bus.routes = routes
                    
                    # Get availability info
                    confirmed_bookings = bus.booking_set.filter(
                        date=today,
                        status='confirmed'
                    ).count()
                    
                    bus.available_seats = max(0, bus.capacity - confirmed_bookings)
                    bus.is_available = bus.available_seats > 0
                    buses_with_info.append(bus)
            
            context['buses'] = buses_with_info
            return context
            
        except Exception as e:
            logger.error(f"Error in get_context_data: {str(e)}")
            raise ValidationError("An error occurred while preparing the page data.")

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            logger.warning(f"Unauthenticated access attempt from IP: {self.request.META.get('REMOTE_ADDR')}")
            return super().handle_no_permission()
        logger.warning(f"Unauthorized access attempt by user {self.request.user.id}")
        raise PermissionDenied("Only active students can access this page. Please create a student profile first.")
