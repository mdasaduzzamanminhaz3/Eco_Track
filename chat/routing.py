from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Using the pickup request UUID as the chat room URL
    re_path(r'^ws/chat/(?P<pickup_id>[a-f0-9\-]+)/$', consumers.ChatConsumer.as_asgi()),
]