from rest_framework import serializers
from .models import Conference, Tickets, Attendee, CustomerTicket, Payment


class ConferenceSerializer(serializers.ModelSerializer):
    """Serializer for Conference model"""
    tickets_available = serializers.SerializerMethodField()
    ticket_price = serializers.SerializerMethodField()
    total_tickets = serializers.SerializerMethodField()
    
    class Meta:
        model = Conference
        fields = ['id', 'name', 'date', 'location', 'tickets_available', 'ticket_price', 'total_tickets']
    
    def get_tickets_available(self, obj):
        """Get total available tickets for this conference"""
        return sum(ticket.quantity_available for ticket in obj.tickets_set.all())
    
    def get_ticket_price(self, obj):
        """Get the price of the first available ticket"""
        first_ticket = obj.tickets_set.filter(quantity_available__gt=0).first()
        return str(first_ticket.price) if first_ticket else None
    
    def get_total_tickets(self, obj):
        """Get total tickets for this conference"""
        return obj.tickets_set.count()


class TicketsSerializer(serializers.ModelSerializer):
    """Serializer for Tickets model"""
    conference_name = serializers.CharField(source='conference.name', read_only=True)
    conference_date = serializers.DateField(source='conference.date', read_only=True)
    conference_location = serializers.CharField(source='conference.location', read_only=True)
    
    class Meta:
        model = Tickets
        fields = ['id', 'conference', 'conference_name', 'conference_date', 'conference_location', 'price', 'quantity_available']


class AttendeeSerializer(serializers.ModelSerializer):
    """Serializer for Attendee model"""
    full_name = serializers.SerializerMethodField()
    total_bookings = serializers.SerializerMethodField()
    
    class Meta:
        model = Attendee
        fields = ['id', 'first_name', 'last_name', 'email', 'full_name', 'total_bookings']
    
    def get_full_name(self, obj):
        """Get full name of attendee"""
        return f"{obj.first_name} {obj.last_name}"
    
    def get_total_bookings(self, obj):
        """Get total bookings for this attendee"""
        return obj.customerticket_set.count()


class CustomerTicketSerializer(serializers.ModelSerializer):
    """Serializer for CustomerTicket model"""
    attendee = AttendeeSerializer(read_only=True)
    conference_name = serializers.CharField(source='ticket.conference.name', read_only=True)
    conference_date = serializers.DateField(source='ticket.conference.date', read_only=True)
    conference_location = serializers.CharField(source='ticket.conference.location', read_only=True)
    ticket_price = serializers.DecimalField(source='ticket.price', max_digits=6, decimal_places=2, read_only=True)
    
    class Meta:
        model = CustomerTicket
        fields = [
            'id', 'attendee', 'ticket', 'conference_name', 'conference_date', 
            'conference_location', 'ticket_price', 'ticket_number', 
            'ticket_status', 'purchase_date'
        ]


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model"""
    attendee = AttendeeSerializer(read_only=True)
    attendee_name = serializers.CharField(source='attendee.first_name', read_only=True)
    attendee_email = serializers.CharField(source='attendee.email', read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'attendee', 'attendee_name', 'attendee_email', 'amount', 'payment_date', 'payment_method']


class BookingCreateSerializer(serializers.Serializer):
    """Serializer for creating a new booking"""
    conference_id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    payment_method = serializers.ChoiceField(choices=[
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ])
    
    def validate_conference_id(self, value):
        """Validate that conference exists and has available tickets"""
        try:
            conference = Conference.objects.get(id=value)
            # Check if conference has available tickets using the reverse relationship
            available_tickets = Tickets.objects.filter(
                conference=conference, 
                quantity_available__gt=0
            )
            if not available_tickets.exists():
                raise serializers.ValidationError("No tickets available for this conference")
            return value
        except Conference.DoesNotExist:
            raise serializers.ValidationError("Conference not found")
    
    def validate_email(self, value):
        """Validate email format"""
        if '@' not in value:
            raise serializers.ValidationError("Please enter a valid email address")
        return value.lower()


class BookingResponseSerializer(serializers.Serializer):
    """Serializer for booking response"""
    success = serializers.BooleanField()
    message = serializers.CharField()
    ticket_number = serializers.CharField(required=False)
    customer_ticket = CustomerTicketSerializer(required=False)
    payment = PaymentSerializer(required=False)
    errors = serializers.DictField(required=False)


class ConferenceStatsSerializer(serializers.Serializer):
    """Serializer for conference statistics"""
    total_conferences = serializers.IntegerField()
    available_conferences = serializers.IntegerField()
    total_bookings = serializers.IntegerField()
    total_attendees = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    recent_bookings = CustomerTicketSerializer(many=True)


class TicketCheckSerializer(serializers.Serializer):
    """Serializer for ticket check response"""
    found = serializers.BooleanField()
    message = serializers.CharField(required=False)
    ticket = CustomerTicketSerializer(required=False)