from django.urls import re_path
from djangochannelsrestframework.consumers import view_as_consumer

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatRoomConsumer.as_asgi()),

]