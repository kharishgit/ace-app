from celery import shared_task
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import sched
import time

@shared_task
def my_celery_task(param1, param2):
    # Your task logic here
    print("hhhhhhh")
    result = param1 + param2
    print(result)
    channel_layer = get_channel_layer()
    print(channel_layer,"hhhhh")
    # ser=PollFightSubmitSerializer(instance,many=False)
    # data=json.dumps(ser.data)
    async_to_sync(channel_layer.group_send)(
        f"test",  # Use the recipient's group
        {"type": "group_message", "message": json.dumps({"action":"refresh-qr","message":"Hi"})}
    )
    print("hhhhhhh")
    return result

scheduler = sched.scheduler(time.time, time.sleep)

def send_message():
    # Send your message to the device via WebSocket
    # You can use the WebSocket connection to send messages to the device here
    print("Hi")
    channel_layer = get_channel_layer()
    print(channel_layer,"hhhhh")
    # ser=PollFightSubmitSerializer(instance,many=False)
    # data=json.dumps(ser.data)
    async_to_sync(channel_layer.group_send)(
        f"test",  # Use the recipient's group
        {"type": "group_message", "message": json.dumps({"action":"pollfight-answer-submit","message":"Hi"})}
    )
    # Schedule the next message sending
    scheduler.enter(15, 1, send_message)
    return
scheduler.enter(15, 1, send_message)