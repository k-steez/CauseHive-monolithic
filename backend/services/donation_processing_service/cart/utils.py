import requests
from rest_framework import serializers
from django.conf import settings

def validate_user_id_with_service(value):
    user_service_url = getattr(settings, 'USER_SERVICE_URL', 'http://localhost:8001/user-service/api/auth')
    url = f"{user_service_url}/users/{value}/"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise serializers.ValidationError('User not found in user service.')
        user_data = response.json()
        if not user_data.get('is_user', False):
            raise serializers.ValidationError('User is not valid.')
    except requests.RequestException:
        raise serializers.ValidationError('User service is not reachable.')
    return value

def validate_event_with_service(value):
    event_service_url = getattr(settings, 'EVENT_SERVICE_URL', 'http://localhost:8000/events-causes-service/events')
    url = f"{event_service_url}/events/{value}/"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise serializers.ValidationError('Event service is not reachable.')
        event_data = response.json()
        if not event_data.get('is_event', False):
            raise serializers.ValidationError('Event is not valid.')
    except requests.RequestException:
        raise serializers.ValidationError('Event service is not reachable.')
    return value

def validate_cause_with_service(value):
    cause_service_url = getattr(settings, 'CAUSE_SERVICE_URL', 'http://localhost:8000/events-causes-service/causes')
    url = f"{cause_service_url}/causes/{value}/"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise serializers.ValidationError('Cause service is not reachable.')
        cause_data = response.json()
        if not cause_data.get('is_cause', False):
            raise serializers.ValidationError('Cause is not valid.')
    except requests.RequestException:
        raise serializers.ValidationError('Cause service is not reachable.')
    return value