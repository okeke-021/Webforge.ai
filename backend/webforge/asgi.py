"""
ASGI config for webforge project.
Handles both HTTP and WebSocket connections.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webforge.settings.development')

django_asgi_app = get_asgi_application()

from apps.generator import routing as generator_routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                generator_routing.websocket_urlpatterns
            )
        )
    ),
})
