import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import plague.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cropguard_backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            plague.routing.websocket_urlpatterns
        )
    ),
})
