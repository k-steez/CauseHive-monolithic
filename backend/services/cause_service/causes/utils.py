import requests
from rest_framework import serializers
from django.conf import settings

def validate_organizer_id_with_service(value):
    user_service_url = getattr(settings, 'USER_SERVICE_URL', 'http://localhost:8000/user/api/auth')
    url = f"{user_service_url}/users/{value}/"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise serializers.ValidationError('Organizer not found in user service.')
        user_data = response.json()
        if not user_data.get('is_organizer', False):
            raise serializers.ValidationError('User is not an organizer.')
    except requests.RequestException:
        raise serializers.ValidationError('User service is not reachable.')
    return value