from channels.generic.websocket import WebsocketConsumer
from channels.consumer import AsyncConsumer
from asgiref.sync import async_to_sync
import json
from django.core.validators import ValidationError
from .models import User

from django.contrib.auth.models import Group

from channels.auth import login

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.list=[]
        group = self.scope['url_route']['kwargs']['groupname']
        self.room_name=group
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        print(f'{self.channel_name}')
        user = self.scope['user']

        self.accept()

    def disconnect(self, close_code):
        group = self.scope['url_route']['kwargs']['groupname']
        self.room_name=group
        print(f'{self.channel_name}  User is not Exists in {group}')
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)

    def receive(self, text_data):
        print(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
             'type':'chat_message1',
            'message': text_data,
            }
        )
      

    def chat_message1(self, event):
        message = event['message']
        data = json.loads(message)
        self.list.append({"message":data['message']})
        print(self.list)
        user=self.scope['user']
        id = User.objects.get(username=user)
        id1 = id.id
        reciver_user_id=data['id']
        print(reciver_user_id)
        self.send(text_data=json.dumps({
        'message':data['message'],
            'id': id1,
            'recerid':data['id']

    }))