from .views import PaystackWebhookView, InitiatePaymentView, VerifyPaymentView
from django.urls import path

urlpatterns = [
    path('webhook/', PaystackWebhookView.as_view(), name='paystack_webhook'),
    path('initiate/', InitiatePaymentView.as_view(), name='initiate_payment'),
    path('verify/<str:reference>/', VerifyPaymentView.as_view(), name='verify_payment'),
]