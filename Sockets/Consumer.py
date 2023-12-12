

from channels.generic.websocket import AsyncWebsocketConsumer
import urllib.parse
import json
from student.tasks import my_celery_task , scheduler
class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("lllllllllllllllllllllllllllllllllllll")
        self.group_name = "test"  # Assign a group name to the consumer
        print(self.channel_name,"lllllllllllllllll")
        # Add the consumer to the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        # my_celery_task.delay(1,2)
        await self.accept()
        # scheduler.run()


    async def disconnect(self, close_code):
        # Remove the consumer from the group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'group_message',
                'message': json.dumps({"action":"disconnect","message":"disconnect"})
            }
        )
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        # Broadcast the received message to the group
        print(text_data,"lllllllllll")
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'group_message',
                'message': text_data
            }
        )


    async def group_message(self, event):
        # Send the message to all consumers in the group
        print(event,"eventssss")
        await self.send(text_data=event['message'])

    async def custom_message(self, event):
        # Send the message to all consumers in the group
        print(event,"11111111111")
        await self.send(text_data=event['message'])


webins= MyConsumer()

class PollFightConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("lllllllllllllllllllllllllllllllllllll")
        query_params = self.scope['query_string']

        # If you want to parse the query parameters into a dictionary, you can use the urllib.parse.parse_qs function
        
        parsed_query_params = urllib.parse.parse_qs(query_params.decode('utf-8'))

        # Now you can access individual query parameters as needed
        param_value = parsed_query_params.get('token', [None])[0]
        print(param_value,"hhhhhhhhhhhhhhhhhhh")
        # print(AuthHandlerIns.decode_token(token=param_value)['id'])
        from accounts.api.authhandle import AuthHandlerIns
        self.group_name = str(AuthHandlerIns.decode_token(token=param_value)['id']) # Assign a group name to the consumer
        # self.group_name=param_value

        # Add the consumer to the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Remove the consumer from the group
        print("hhhhhhhhh")
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'group_message',
                'message': json.dumps({"action":"disconnect","message":"disconnect"})
            }
        )
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        # Broadcast the received message to the group
        print(text_data,"lllllllllll")
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'group_message',
                'message':text_data
            }
        )


    async def group_message(self, event):
        # Send the message to all consumers in the group
        print(event,"eventssss")
        await self.send(text_data=event['message'])



    


pollins= PollFightConsumer()

from asgiref.sync import sync_to_async
class GroupChatConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def get_groups(self, user_id):
        from MobileApp.models import Groups
        return list(Groups.objects.filter(members=user_id).values_list('id', flat=True))

    async def connect(self):
        # ...
        query_params = self.scope['query_string']

        # If you want to parse the query parameters into a dictionary, you can use the urllib.parse.parse_qs function
        
        parsed_query_params = urllib.parse.parse_qs(query_params.decode('utf-8'))

        # Now you can access individual query parameters as needed
        param_value = parsed_query_params.get('token', [None])[0]
        from accounts.api.authhandle import AuthHandlerIns
        user_id = AuthHandlerIns.decode_token(token=param_value)['id']
        
        # Fetch the groups in a synchronous context
        groups = await self.get_groups(user_id)

        for group_id in groups:
            # Add the consumer to the group
            await self.channel_layer.group_add(
                "Group"+str(group_id),
                self.channel_name
            )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the consumer from the group
        print("hhhhhhhhh")
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'group_message',
                'message': json.dumps({"action":"disconnect","message":"disconnect"})
            }
        )
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        # Broadcast the received message to the group
        print(text_data,"lllllllllll")
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'group_message',
                'message':text_data
            }
        )


    async def group_message(self, event):
        # Send the message to all consumers in the group
        print(event,"eventssss")
        await self.send(text_data=event['message'])



    


grpins= GroupChatConsumer()

# from .celery import scheduler

# scheduler.run()
# from .celery import my_celery_task

# result = my_celery_task.delay(1, 2)