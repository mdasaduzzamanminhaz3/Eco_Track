from django.db import models
import uuid
from django.conf import settings
from waste.models import PickupRequest
# Create your models here.

class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Chatting under a pickup request
    pickup_request = models.ForeignKey(PickupRequest, on_delete=models.CASCADE, related_name='chat_messages')
    # Who sent the message (User or Recycler)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='sent_messages')

    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at'] #Previous messages will be shown first (chronological order)
        indexes = [
            models.Index(fields=['pickup_request', 'created_at']), # Database indexing to keep chat speed fast
        ]
def __str__(self):
        return f"From {self.sender.email} for Pickup {self.pickup_request.id[:8]}... at {self.created_at.strftime('%H:%M')}"