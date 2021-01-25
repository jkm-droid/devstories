from django.contrib import admin

from chat.models import ChatRoom, Messages, OnlineUsers

admin.site.register(
    ChatRoom, list_display=['title']
)

admin.site.register(
    Messages, list_display=['sender', 'content', 'chatroom', 'room_id', 'timestamp']
)

admin.site.register(
    OnlineUsers, list_display=['user', 'online_status', 'first_active', 'last_active']
)
