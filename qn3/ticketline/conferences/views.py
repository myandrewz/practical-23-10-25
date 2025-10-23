from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from .models import Conference, Tickets, Attendee, CustomerTicket, Payment
import uuid
import random
import string


def conference_list(request):
    """Step 1: Display all available conferences"""
    conferences = Conference.objects.filter(
        tickets__quantity_available__gt=0
    ).distinct().order_by('date')
    
    return render(request, 'conferences/conference_list.html', {
        'conferences': conferences
    })


def attendee_details(request, conference_id):
    """Step 2: Collect attendee information"""
    conference = get_object_or_404(Conference, id=conference_id)
    ticket = get_object_or_404(Tickets, conference=conference, quantity_available__gt=0)
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        
        # Basic validation
        errors = {}
        if not first_name:
            errors['first_name'] = 'First name is required'
        if not last_name:
            errors['last_name'] = 'Last name is required'
        if not email:
            errors['email'] = 'Email is required'
        
        if not errors:
            # Store data in session for next step
            request.session['booking_data'] = {
                'conference_id': conference_id,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            }
            request.session.modified = True
            return redirect('payment', conference_id=conference_id)
        
        # If there are errors, render form with errors
        form_data = {
            'first_name': {'value': first_name, 'errors': errors.get('first_name')},
            'last_name': {'value': last_name, 'errors': errors.get('last_name')},
            'email': {'value': email, 'errors': errors.get('email')},
        }
        
        return render(request, 'conferences/attendee_details.html', {
            'conference': conference,
            'ticket': ticket,
            'form': form_data,
        })
    
    return render(request, 'conferences/attendee_details.html', {
        'conference': conference,
        'ticket': ticket,
        'form': {},
    })


def payment(request, conference_id):
    """Step 3: Handle payment processing"""
    conference = get_object_or_404(Conference, id=conference_id)
    ticket = get_object_or_404(Tickets, conference=conference, quantity_available__gt=0)
    
    # Get booking data from session
    booking_data = request.session.get('booking_data')
    if not booking_data or booking_data.get('conference_id') != conference_id:
        messages.error(request, 'Session expired. Please start over.')
        return redirect('conference_list')
    
    # Create or get attendee object for display
    attendee_data = {
        'first_name': booking_data['first_name'],
        'last_name': booking_data['last_name'],
        'email': booking_data['email'],
    }
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', '').strip()
        terms_accepted = request.POST.get('terms')
        
        # Validation
        if not payment_method:
            messages.error(request, 'Please select a payment method.')
            return render(request, 'conferences/payment.html', {
                'conference': conference,
                'ticket': ticket,
                'attendee': attendee_data,
            })
        
        if not terms_accepted:
            messages.error(request, 'Please accept the terms and conditions.')
            return render(request, 'conferences/payment.html', {
                'conference': conference,
                'ticket': ticket,
                'attendee': attendee_data,
            })
        
        # Process the booking
        try:
            with transaction.atomic():
                # Create or get attendee
                attendee, created = Attendee.objects.get_or_create(
                    email=booking_data['email'],
                    defaults={
                        'first_name': booking_data['first_name'],
                        'last_name': booking_data['last_name'],
                    }
                )
                
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
                payment_record = Payment.objects.create(
                    attendee=attendee,
                    amount=ticket.price,
                    payment_method=payment_method
                )
                
                # Update ticket quantity
                ticket.quantity_available -= 1
                ticket.save()
                
                # Store success data in session using ticket_number (which is unique)
                request.session['success_data'] = {
                    'ticket_number': customer_ticket.ticket_number,
                    'attendee_email': attendee.email,
                }
                request.session.modified = True
                
                # Clear booking data
                if 'booking_data' in request.session:
                    del request.session['booking_data']
                
                return redirect('booking_success')
                
        except Exception as e:
            messages.error(request, f'Payment processing failed: {str(e)}')
            return render(request, 'conferences/payment.html', {
                'conference': conference,
                'ticket': ticket,
                'attendee': attendee_data,
            })
    
    return render(request, 'conferences/payment.html', {
        'conference': conference,
        'ticket': ticket,
        'attendee': attendee_data,
    })


def booking_success(request):
    """Step 4: Display booking confirmation"""
    success_data = request.session.get('success_data')
    if not success_data:
        messages.error(request, 'No booking found.')
        return redirect('conference_list')
    
    try:
        # Look up by ticket number instead of ID
        customer_ticket = CustomerTicket.objects.get(
            ticket_number=success_data['ticket_number']
        )
        payment = Payment.objects.filter(
            attendee__email=success_data['attendee_email']
        ).latest('payment_date')
        
        # Clear success data from session
        if 'success_data' in request.session:
            del request.session['success_data']
            request.session.modified = True
        
        return render(request, 'conferences/success.html', {
            'customer_ticket': customer_ticket,
            'payment': payment,
        })
        
    except (CustomerTicket.DoesNotExist, Payment.DoesNotExist):
        messages.error(request, 'Booking details not found.')
        return redirect('conference_list')


def generate_ticket_number():
    """Generate a unique ticket number"""
    while True:
        # Generate format: CONF-YYYYMMDD-XXXXX
        date_str = timezone.now().strftime('%Y%m%d')
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        ticket_number = f"CONF-{date_str}-{random_str}"
        
        # Check if this number already exists
        if not CustomerTicket.objects.filter(ticket_number=ticket_number).exists():
            return ticket_number