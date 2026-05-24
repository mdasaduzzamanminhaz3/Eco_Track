from django.db import models
import uuid
from django.conf import settings
# Create your models here.

class WasteCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    carbon_multiplier = models.FloatField(default=0.0, verbose_name="CO2 Saved per KG")
    points_multiplier = models.IntegerField(default=0,verbose_name="Points per KG")

    class Meta: 
        verbose_name_plural ="Waste Categories"

    def __str__(self):
        return self.name

class PickupRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('COLLECTED', 'Collected'),
        ('CANCELLED', 'Cancelled'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='pickup_requests',verbose_name="Normal User")
    recycler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='collected_pickups',verbose_name="Assigned Recycler")
    category = models.ForeignKey(WasteCategory, on_delete=models.PROTECT,verbose_name="Waste Category")

    estimated_weight = models.FloatField(verbose_name="Estimated Weight (KG)")
    actual_weight = models.FloatField(null=True, blank=True,verbose_name="Actual Weight (Recycler Verified in KG)")
    pickup_address = models.TextField(verbose_name="Pickup Address/Notes")
    latitude = models.DecimalField(max_digits=9,decimal_places=6,null=True, blank=True,verbose_name="Latitude")
    longitude = models.DecimalField(max_digits=9,decimal_places=6,null=True, blank=True,verbose_name="Longitude")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING',verbose_name="Request Status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Pickup #{str(self.id)[:8]} - {self.user.email} ({self.status})"