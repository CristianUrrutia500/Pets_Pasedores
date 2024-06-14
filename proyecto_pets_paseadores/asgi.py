# asgi.py

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import proyecto_pets_paseadores

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_pets_paseadores.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            proyecto_pets_paseadores.routing.websocket_urlpatterns
        )
    ),
})
