from django.urls import re_path
from chatrest import consumers

websocket_urlpatterns = [
    re_path(r"^ws/$", consumers.UserConsumer.as_asgi()),
]