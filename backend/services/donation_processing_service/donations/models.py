from django.db import models

# Create your models here.
class Donation(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    user_id = models.UUIDField(db_index=True, editable=False)
    cause_id = models.UUIDField(db_index=True, editable=False)  # References either an event or cause ID from the event_causes_services
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='GHS')  # Default currency is GHS
    donated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='pending')
    recipient_id = models.UUIDField(db_index=True, editable=False)
    transaction_id = models.CharField(max_length=255, unique=True, null=True, blank=True)  # Unique transaction ID from payment gateway