import sched
import time

# Create a scheduler
# scheduler = sched.scheduler(time.time, time.sleep)

# # Define a function to send a message
# def send_message():
#     # Send your message to the device via WebSocket
#     # You can use the WebSocket connection to send messages to the device here
#     print("Hi")
#     # Schedule the next message sending
#     scheduler.enter(60, 1, send_message)

# # Schedule the initial message sending
# scheduler.enter(0, 1, send_message)

# # Start the scheduler
# scheduler.run()

from celery import shared_task
from aceapp.celery import app
from celery import Celery
import logging
import requests
from aceapp.settings.base import vimeo_access_token
from MobileApp.serializers import stream_vimeo_video


@shared_task
def my_celery_task(param1, param2):
    # Your task logic here
    result = param1 + param2
    print(result)
    return result

logger = logging.getLogger(__name__)

@app.task(bind=True, max_retries=3)  # Set max_retries to limit the number of retries
def check_video_upload_task(self):
    # Simulate checking if the video is uploaded
    try:
        access_token = vimeo_access_token

        headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.vimeo.*+json;version=3.4',
        }
        response = requests.get('https://api.vimeo.com/videos/866283435?fields=uri,upload.status,transcode.status', headers=headers,  verify=False)
        status = response.json()['transcode']
        print(status,"   status")
        if status['status'] == 'complete':
            print("Condition met, returning True")
            video = stream_vimeo_video(866283435)
            print(video,"  ooooooooooopppppp")
            return True
        else:
            # print(vimeo_id," id ")
            
            # If the video is not uploaded, retry the task after a delay
            # The task will be retried up to max_retries times with exponential backoff
            check_video_upload_task.apply_async(countdown=2) 
            
    except Exception as e:
        logger.error(e," 90000000000000000")
        self.retry(exc=e)

from celery import shared_task
from django.core.mail import send_mail

def send_daily_emails():
    recipients = ['com.harishk@gmail.com']
    subject = 'Your Daily Email'
    message = 'This is your daily email content.'

    for recipient in recipients:
        send_mail(subject, message, 'ashlymathew28122001@gmail.com', [recipient])