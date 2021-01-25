from django.contrib import messages
import json
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from chat.models import ChatRoom, Messages
from portal.views import get_notifications


def show_chat_view(request):
    if request.user.is_authenticated:
        template_name = "chat/chatindex.html"
        darkmode = True
        notice = get_notifications()
        rooms = ChatRoom.objects.all()

        context = {
            'darkmode': darkmode,
            'notice': notice,
            'rooms': rooms
        }

        return render(request, template_name, context)
    else:
        messages.info(request, "You must be logged in")
        return redirect('login')


def chat_room_view(request, title):
    if request.user.is_authenticated:
        template_name = 'chat/chat-room-1.html'
        darkmode = True

        room_name = title
        room_title = title

        context = {
            'room_name': room_name,
            'username': mark_safe(json.dumps(request.user.username)),
            'room_title': room_title,
            'darkmode': darkmode
        }

        return render(request, template_name, context)
    else:
        messages.info(request, "You must be logged in")
        return redirect('login')
