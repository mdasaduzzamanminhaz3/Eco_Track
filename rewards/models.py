from django.db import models
from django.conf import settings
import uuid
from waste.models import PickupRequest
# Create your models here.
class UserWallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='wallet')
    total_points = models.IntegerField(default=0, verbose_name='Total Earned  Points')
    current_points = models.IntegerField(default=0, verbose_name='Current Redeemable Points')
    total_carbon_saved = models.FloatField(default=0.0, verbose_name='Total Carbon Saved (kg)')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s wallet - {self.current_points} pts"
    
class TransactionHistory(models.Model):
    TRANSACTION_TYPES = (
        ('EARNED', 'Earned from waste'),
        ('REDEEMED', 'Redeemed Prize'),
    )

    id = models.UUIDfield(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(UserWallet, on_delete=models.CASCADE, related_name='transactions')
    pickup_request = models.ForeignKey(PickupRequest, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, default ='EARNED')
    points = models.IntegerField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type} - {self.points} Pts ({self.wallet.user.email})"