from django.db import models
from donations.models import Donation

# Create your models here.
class PaymentTransaction(models.Model):
    id =  models.UUIDField(primary_key=True, editable=False)
    donation = models.OneToOneField(Donation, on_delete=models.CASCADE)
    user_id = models.UUIDField(db_index=True, editable=False)  # User who made the donation
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='GHS')  # The Default currency is GHS
    transaction_id = models.CharField(max_length=255, unique=True)  # Unique transaction ID from payment gateway
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='pending')
    transaction_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment for {self.donation} by {self.user_id} - {self.status}"