from django.urls import re_path
from djangochannelsrestframework.consumers import view_as_consumer

from chatrest import consumers
from chatrest.views import UserViewSet

websocket_urlpatterns = [
    re_path(r"^ws/my-consumer/$", consumers.MyConsumer.as_asgi()),
    # re_path(r"^ws/$", consumers.UserConsumerObserver.as_asgi()),
    # re_path(r"^user/$", view_as_consumer(UserViewSet.as_view({'get': 'list'})))
]