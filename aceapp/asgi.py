"""
ASGI config for aceapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from Sockets.urls import websocket_urlpatterns
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aceapp.settings')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aceapp.settings.local')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(websocket_urlpatterns),
})


