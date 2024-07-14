from django.core.management.base import BaseCommand, CommandError

from django_zoom_meetings import ZoomMeetings
from datetime import datetime

import jwt
import requests
import json
from time import time

# Enter your API key and your API secret
API_KEY = 'fDanOZ4XTxWJdc_0b9Ghgg'
API_SEC = 'H3pKDb93EnYJsmEYar1r11tEqI33vJmU'


def generate_token(api_key, api_secret):
    url = f'https://api.zoom.us/v2/users/{API_KEY}/token?type=zak'
    response = requests.post(url, headers={'Authorization': f'Bearer {API_SEC}'})
    print(response)
    return response.json()['token']


token = generate_token(API_KEY, API_SEC)


def schedule_meeting(token, topic, start_time, duration):
    url = 'https://api.zoom.us/v2/users/me/meetings'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        'topic': topic,
        'type': 2,
        'start_time': start_time,
        'duration': duration
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        meeting_info = schedule_meeting(token, 'Python Automation Meeting', '2024-04-28T10:00:00Z', 60)
        print("Meeting ID:", meeting_info['id'])
