# chat/routing.py
from django.urls import re_path, path
from . import consumers
websocket_urlpatterns = [
    re_path(r'ws/kakao/(?P<browser_id>\w+)/$',
            consumers.KakaoConsumer.as_asgi()),
]
