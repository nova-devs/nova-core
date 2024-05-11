import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from nova.routing import urlrouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nova.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(urlrouter),
})
