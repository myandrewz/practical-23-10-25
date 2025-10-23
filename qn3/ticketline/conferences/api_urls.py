from django.urls import path
from . import api_views

urlpatterns = [
    # Conference endpoints
    path('conferences/', api_views.ConferenceListAPIView.as_view(), name='api_conference_list'),
    path('conferences/all/', api_views.AllConferencesAPIView.as_view(), name='api_all_conferences'),
    path('conferences/<int:pk>/', api_views.ConferenceDetailAPIView.as_view(), name='api_conference_detail'),
    path('conferences/<int:conference_id>/bookings/', api_views.conference_bookings, name='api_conference_bookings'),
    path('conferences/search/', api_views.search_conferences, name='api_search_conferences'),
    
    # Tickets endpoints
    path('conferences/<int:conference_id>/tickets/', api_views.TicketsListAPIView.as_view(), name='api_conference_tickets'),
    path('tickets/', api_views.AllTicketsAPIView.as_view(), name='api_all_tickets'),
    
    # Attendee endpoints
    path('attendees/', api_views.AttendeeListAPIView.as_view(), name='api_attendee_list'),
    path('attendees/<int:pk>/', api_views.AttendeeDetailAPIView.as_view(), name='api_attendee_detail'),
    path('attendees/<int:attendee_id>/bookings/', api_views.attendee_bookings, name='api_attendee_bookings'),
    
    # Booking endpoints
    path('booking/', api_views.BookingAPIView.as_view(), name='api_booking_create'),
    path('bookings/', api_views.CustomerTicketListAPIView.as_view(), name='api_customer_tickets'),
    path('bookings/<str:ticket_number>/', api_views.CustomerTicketDetailAPIView.as_view(), name='api_ticket_detail'),
    
    # Payment endpoints
    path('payments/', api_views.PaymentListAPIView.as_view(), name='api_payments'),
    path('payments/<int:pk>/', api_views.PaymentDetailAPIView.as_view(), name='api_payment_detail'),
    
    # Utility endpoints
    path('stats/', api_views.api_stats, name='api_stats'),
    path('check-ticket/<str:ticket_number>/', api_views.check_ticket, name='api_check_ticket'),
    path('cancel-ticket/<str:ticket_number>/', api_views.cancel_ticket, name='api_cancel_ticket'),
]