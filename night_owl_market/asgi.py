"""
ASGI config for night_owl_market project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'night_owl_market.settings')
django.setup()

django_asgi_app = get_asgi_application()

from .channels_middleware import JwtAuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import market.routing

application = ProtocolTypeRouter({
  'https': django_asgi_app,
  'websocket': AllowedHostsOriginValidator(
    JwtAuthMiddlewareStack(
        URLRouter(
            market.routing.websocket_urlpatterns
        ),
    )
  )
})
