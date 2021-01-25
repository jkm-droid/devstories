from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ChatRoom(models.Model):
    title = models.CharField(max_length=50)
    created_on = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    def absolute_url(self):
        return f"/chat/{self.title}/"


class Messages(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    content = models.TextField()
    chatroom = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    class Meta:
        ordering = ('timestamp',)


class OnlineUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    STATUS = (
        ("ONLINE", "online"),
        ("OFFLINE", "offline"),
    )
    online_status = models.CharField(max_length=10, choices=STATUS, default="OFFLINE")
    # device_id = models.CharField(max_length=150)
    first_active = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)