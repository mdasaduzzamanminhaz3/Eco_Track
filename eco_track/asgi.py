"""
ASGI config for eco_track project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing 
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eco_track.settings')
os.environ.setdefault('django.settings.module', 'config.settings.settings')

# application = get_asgi_application()


# Separating HTTP and WebSocket routing
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})