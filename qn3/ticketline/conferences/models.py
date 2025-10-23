from django.db import models

class Conference(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    
class Tickets(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity_available = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.price} for {self.conference.name}"
    

class Attendee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class CustomerTicket(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=50, unique=True)
    ticket_status = models.CharField(max_length=20, choices=[('purchased', 'Purchased'), ('cancelled', 'Cancelled')], default='purchased')
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attendee} - {self.ticket}"
    
    
class Payment(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment of {self.amount} by {self.attendee}"
    

