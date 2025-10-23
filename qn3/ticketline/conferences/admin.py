from django.contrib import admin
from .models import Conference, Tickets, Attendee, CustomerTicket, Payment


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location')
    list_filter = ('date', 'location')
    search_fields = ('name', 'location')
    date_hierarchy = 'date'
    ordering = ('date',)


@admin.register(Tickets)
class TicketsAdmin(admin.ModelAdmin):
    list_display = ('conference', 'price', 'quantity_available')
    list_filter = ('conference', 'price')
    search_fields = ('conference__name',)
    list_editable = ('price', 'quantity_available')
    ordering = ('conference', 'price')


@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('last_name', 'first_name')


@admin.register(CustomerTicket)
class CustomerTicketAdmin(admin.ModelAdmin):
    list_display = ('attendee', 'ticket', 'ticket_number', 'ticket_status', 'purchase_date')
    list_filter = ('ticket_status', 'purchase_date', 'ticket__conference')
    search_fields = ('attendee__first_name', 'attendee__last_name', 'ticket_number')
    date_hierarchy = 'purchase_date'
    ordering = ('-purchase_date',)
    readonly_fields = ('ticket_number', 'purchase_date')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('attendee', 'amount', 'payment_date', 'payment_method')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('attendee__first_name', 'attendee__last_name')
    date_hierarchy = 'payment_date'
    ordering = ('-payment_date',)
    readonly_fields = ('payment_date',)

