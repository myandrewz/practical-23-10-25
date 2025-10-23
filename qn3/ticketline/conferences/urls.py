from django.urls import path, include
from . import views

urlpatterns = [
    # Web interface URLs
    path('', views.conference_list, name='conference_list'),
    path('book/<int:conference_id>/', views.attendee_details, name='attendee_details'),
    path('payment/<int:conference_id>/', views.payment, name='payment'),
    path('success/', views.booking_success, name='booking_success'),
    
    # API URLs
    path('api/', include('conferences.api_urls')),
]