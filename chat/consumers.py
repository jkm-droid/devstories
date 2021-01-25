from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from portal.models import UserProfile
from .models import Messages, OnlineUsers, ChatRoom

User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        room_name = self.scope['url_route']['kwargs']['room_name']
        messages = Messages.objects.filter(chatroom=room_name).order_by('timestamp')

        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }

        self.send_message(content)

    def new_message(self, data):
        sender = data['from']
        chatroom = data['chatroom']
        author_user = User.objects.filter(username=sender)[0]
        message_body = data['message']

        # getting the room, then getting its id
        room = ChatRoom.objects.get(title=chatroom)
        message = Messages.objects.create(
            sender=author_user,
            content=message_body,
            chatroom=chatroom,
            room_id=room.id
        )
        message.save()

        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }

        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        time = message.timestamp

        return {
            'id': message.id,
            'author': message.sender.username,
            'content': message.content,
            'timestamp': str(time.strftime("%I:%M%p"))
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(
            self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        user = self.scope['user']
        # change the online status if user from offline to online
        UserProfile.objects.filter(user=user).update(is_online=True)
        # get the number of users that are online
        users = UserProfile.objects.filter(is_online=True).count()
        print(f"-------------{user} online----------------")
        self.get_online_users(users)

    def disconnect(self, close_code):
        async_to_sync(
            self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        user = self.scope['user']
        # change the online status if user from online to offline
        UserProfile.objects.filter(user=user).update(is_online=False)
        # get the number of users that are online
        users = UserProfile.objects.filter(is_online=True).count()
        print(f"-------------{user} offline----------------")
        self.get_online_users(users)

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(
            self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))

    # update the user status, the status will be
    # either offline or online
    @database_sync_to_async
    def update_user_online_status(self, user, status):
        status_update = OnlineUsers.objects.create(
            user=user,
            online_status=status
        )
        status_update.save()

    def get_online_users(self, no_of_users):
        users = {
            'command': 'get_online_users',
            'no_of_users': no_of_users
        }
        print(json.dumps(users))
        self.send(json.dumps(users))
