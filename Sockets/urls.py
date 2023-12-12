






from django.urls import re_path

from .Consumer import MyConsumer, webins, pollins,grpins


websocket_urlpatterns = [
    # re_path(r'ws/my-websocket/$', MyWebSocketConsumer.as_asgi()),
    re_path(r'new-sock/$', webins.as_asgi()),
    re_path(r'new-grpins/$', grpins.as_asgi()),
    re_path(r'ws/pollfight/$', pollins.as_asgi()),
    # re_path(r'ws/post/$', PostConsumer.as_asgi()),
]
