from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count, Q
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.openapi import OpenApiTypes
from .models import Conference, Tickets, Attendee, CustomerTicket, Payment
from .serializers import (
    ConferenceSerializer, TicketsSerializer, AttendeeSerializer,
    CustomerTicketSerializer, PaymentSerializer, BookingCreateSerializer,
    BookingResponseSerializer, ConferenceStatsSerializer, TicketCheckSerializer
)
from .views import generate_ticket_number


class ConferenceListAPIView(generics.ListAPIView):
    """
    List all available conferences with tickets.
    
    Returns conferences that have available tickets, ordered by date.
    """
    serializer_class = ConferenceSerializer
    
    def get_queryset(self):
        """Return only conferences with available tickets, ordered by date"""
        return Conference.objects.filter(
            tickets__quantity_available__gt=0
        ).distinct().order_by('date')


class ConferenceDetailAPIView(generics.RetrieveAPIView):
    """
    Get detailed information about a specific conference.
    
    Returns conference details including ticket availability and pricing.
    """
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer


class AllConferencesAPIView(generics.ListAPIView):
    """API endpoint to list all conferences (including sold out)"""
    queryset = Conference.objects.all().order_by('date')
    serializer_class = ConferenceSerializer


class TicketsListAPIView(generics.ListAPIView):
    """API endpoint to list tickets for a specific conference"""
    serializer_class = TicketsSerializer
    
    def get_queryset(self):
        conference_id = self.kwargs.get('conference_id')
        return Tickets.objects.filter(
            conference_id=conference_id,
            quantity_available__gt=0
        )


class AllTicketsAPIView(generics.ListAPIView):
    """API endpoint to list all tickets"""
    queryset = Tickets.objects.all().order_by('conference__date')
    serializer_class = TicketsSerializer


class AttendeeListAPIView(generics.ListAPIView):
    """API endpoint to list all attendees"""
    queryset = Attendee.objects.all().order_by('last_name', 'first_name')
    serializer_class = AttendeeSerializer


class AttendeeDetailAPIView(generics.RetrieveAPIView):
    """API endpoint to get a specific attendee"""
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer


class CustomerTicketListAPIView(generics.ListAPIView):
    """API endpoint to list customer tickets"""
    queryset = CustomerTicket.objects.all().order_by('-purchase_date')
    serializer_class = CustomerTicketSerializer


class CustomerTicketDetailAPIView(generics.RetrieveAPIView):
    """API endpoint to get ticket by ticket number"""
    serializer_class = CustomerTicketSerializer
    lookup_field = 'ticket_number'
    
    def get_queryset(self):
        return CustomerTicket.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    """API endpoint to list payments"""
    queryset = Payment.objects.all().order_by('-payment_date')
    serializer_class = PaymentSerializer


class PaymentDetailAPIView(generics.RetrieveAPIView):
    """API endpoint to get a specific payment"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class BookingAPIView(APIView):
    """
    Create a new conference booking.
    
    This endpoint handles the complete booking process including:
    - Attendee creation or retrieval
    - Ticket reservation
    - Payment processing
    - Inventory management
    """
    
    def post(self, request):
        """Create a new booking with payment"""
        serializer = BookingCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Invalid data provided',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        try:
            with transaction.atomic():
                # Get conference and ticket
                conference = get_object_or_404(Conference, id=data['conference_id'])
                ticket = get_object_or_404(
                    Tickets, 
                    conference=conference, 
                    quantity_available__gt=0
                )
                
                # Create or get attendee
                attendee, created = Attendee.objects.get_or_create(
                    email=data['email'],
                    defaults={
                        'first_name': data['first_name'],
                        'last_name': data['last_name'],
                    }
                )
                
                # If attendee exists but names are different, update them
                if not created:
                    attendee.first_name = data['first_name']
                    attendee.last_name = data['last_name']
                    attendee.save()
                
                # Generate unique ticket number
                ticket_number = generate_ticket_number()
                
                # Create customer ticket
                customer_ticket = CustomerTicket.objects.create(
                    attendee=attendee,
                    ticket=ticket,
                    ticket_number=ticket_number,
                    ticket_status='purchased'
                )
                
                # Create payment record
                payment = Payment.objects.create(
                    attendee=attendee,
                    amount=ticket.price,
                    payment_method=data['payment_method']
                )
                
                # Update ticket quantity
                ticket.quantity_available -= 1
                ticket.save()
                
                # Prepare response data
                response_data = {
                    'success': True,
                    'message': 'Booking created successfully',
                    'ticket_number': ticket_number,
                    'customer_ticket': CustomerTicketSerializer(customer_ticket).data,
                    'payment': PaymentSerializer(payment).data
                }
                
                return Response(response_data, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Booking failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def api_stats(request):
    """API endpoint for comprehensive statistics"""
    try:
        # Basic stats
        total_conferences = Conference.objects.count()
        available_conferences = Conference.objects.filter(
            tickets__quantity_available__gt=0
        ).distinct().count()
        total_bookings = CustomerTicket.objects.count()
        total_attendees = Attendee.objects.count()
        
        # Revenue calculation
        total_revenue = Payment.objects.aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # Recent bookings (last 10)
        recent_bookings = CustomerTicket.objects.order_by('-purchase_date')[:10]
        
        stats_data = {
            'total_conferences': total_conferences,
            'available_conferences': available_conferences,
            'total_bookings': total_bookings,
            'total_attendees': total_attendees,
            'total_revenue': total_revenue,
            'recent_bookings': CustomerTicketSerializer(recent_bookings, many=True).data
        }
        
        return Response(stats_data)
        
    except Exception as e:
        return Response({
            'error': f'Failed to get stats: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def check_ticket(request, ticket_number):
    """API endpoint to check ticket status"""
    try:
        customer_ticket = CustomerTicket.objects.get(ticket_number=ticket_number)
        return Response({
            'found': True,
            'ticket': CustomerTicketSerializer(customer_ticket).data
        })
    except CustomerTicket.DoesNotExist:
        return Response({
            'found': False,
            'message': f'Ticket {ticket_number} not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def conference_bookings(request, conference_id):
    """API endpoint to get all bookings for a specific conference"""
    try:
        conference = get_object_or_404(Conference, id=conference_id)
        bookings = CustomerTicket.objects.filter(
            ticket__conference=conference
        ).order_by('-purchase_date')
        
        return Response({
            'conference': ConferenceSerializer(conference).data,
            'total_bookings': bookings.count(),
            'bookings': CustomerTicketSerializer(bookings, many=True).data
        })
        
    except Conference.DoesNotExist:
        return Response({
            'error': 'Conference not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def attendee_bookings(request, attendee_id):
    """API endpoint to get all bookings for a specific attendee"""
    try:
        attendee = get_object_or_404(Attendee, id=attendee_id)
        bookings = CustomerTicket.objects.filter(
            attendee=attendee
        ).order_by('-purchase_date')
        
        payments = Payment.objects.filter(
            attendee=attendee
        ).order_by('-payment_date')
        
        return Response({
            'attendee': AttendeeSerializer(attendee).data,
            'total_bookings': bookings.count(),
            'bookings': CustomerTicketSerializer(bookings, many=True).data,
            'payments': PaymentSerializer(payments, many=True).data
        })
        
    except Attendee.DoesNotExist:
        return Response({
            'error': 'Attendee not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def search_conferences(request):
    """API endpoint to search conferences by name or location"""
    query = request.GET.get('q', '')
    
    if not query:
        return Response({
            'error': 'Search query parameter "q" is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    conferences = Conference.objects.filter(
        Q(name__icontains=query) | Q(location__icontains=query)
    ).order_by('date')
    
    return Response({
        'query': query,
        'count': conferences.count(),
        'results': ConferenceSerializer(conferences, many=True).data
    })


@api_view(['POST'])
def cancel_ticket(request, ticket_number):
    """API endpoint to cancel a ticket"""
    try:
        customer_ticket = get_object_or_404(CustomerTicket, ticket_number=ticket_number)
        
        if customer_ticket.ticket_status == 'cancelled':
            return Response({
                'success': False,
                'message': 'Ticket is already cancelled'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            # Update ticket status
            customer_ticket.ticket_status = 'cancelled'
            customer_ticket.save()
            
            # Restore ticket quantity
            ticket = customer_ticket.ticket
            ticket.quantity_available += 1
            ticket.save()
        
        return Response({
            'success': True,
            'message': 'Ticket cancelled successfully',
            'ticket': CustomerTicketSerializer(customer_ticket).data
        })
        
    except CustomerTicket.DoesNotExist:
        return Response({
            'success': False,
            'message': f'Ticket {ticket_number} not found'
        }, status=status.HTTP_404_NOT_FOUND)