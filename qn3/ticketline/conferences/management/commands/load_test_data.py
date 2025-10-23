from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from conferences.models import Conference, Tickets

class Command(BaseCommand):
    help = 'Load test data for conferences'

    def handle(self, *args, **options):
        # Create conferences
        conf1 = Conference.objects.create(
            name="Django Conference 2024",
            date=timezone.now().date() + timedelta(days=30),
            location="San Francisco, CA"
        )
        
        conf2 = Conference.objects.create(
            name="Python Summit 2024",
            date=timezone.now().date() + timedelta(days=45),
            location="New York, NY"
        )
        
        conf3 = Conference.objects.create(
            name="Web Development Bootcamp",
            date=timezone.now().date() + timedelta(days=60),
            location="Austin, TX"
        )
        
        # Create tickets
        Tickets.objects.create(
            conference=conf1,
            price=299,
            quantity_available=100
        )
        
        Tickets.objects.create(
            conference=conf2,
            price=399,
            quantity_available=50
        )
        
        Tickets.objects.create(
            conference=conf3,
            price=199,
            quantity_available=75
        )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded test data!')
        )
        self.stdout.write(f'Created {Conference.objects.count()} conferences')
        self.stdout.write(f'Created {Tickets.objects.count()} ticket types')