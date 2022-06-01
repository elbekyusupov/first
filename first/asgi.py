"""
ASGI config for first project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first.settings')

import chat.routing
import chatrest.routing

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            chatrest.routing.websocket_urlpatterns +
            chat.routing.websocket_urlpatterns,

        ),
        # URLRouter(
        #   chat.routing.websocket_urlpatterns,
        #   # chat.routing.websocket_urlpatterns,
        # ),
    )
})