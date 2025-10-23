from django.urls import path
from . import views

urlpatterns = [
    path('', views.conference_list, name='conference_list'),
    path('book/<int:conference_id>/', views.attendee_details, name='attendee_details'),
    path('payment/<int:conference_id>/', views.payment, name='payment'),
    path('success/', views.booking_success, name='booking_success'),
]