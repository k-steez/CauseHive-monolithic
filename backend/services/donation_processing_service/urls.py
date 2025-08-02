from django.urls import path
from .views import create_donation, get_donation_statistics

urlpatterns = [
    path('api/donations/', create_donation, name='create_donation'),
    path('api/donations/statistics/', get_donation_statistics, name='get_donation_statistics'),
]