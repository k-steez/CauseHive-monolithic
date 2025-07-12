from functools import wraps

import requests
from rest_framework import serializers
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

def validate_user_id_with_service(value, request=None):
    user_service_url = getattr(settings, 'USER_SERVICE_URL', 'http://localhost:8000/user/auth')
    url = f"{user_service_url}/users/{value}/"
    headers = {}
    if request and hasattr(request, 'headers'):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            headers['Authorization'] = auth_header
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise serializers.ValidationError('User not found in user service.')
        user_data = response.json()
        if 'id' in user_data:
            return value
        else:
            raise serializers.ValidationError('User is not valid.')

    except requests.RequestException:
        raise serializers.ValidationError('User service is not reachable.')

    except Exception as e:
        raise serializers.ValidationError(f'An error occurred while validating user: {str(e)}')

def validate_cause_with_service(value, request=None):
    cause_service_url = getattr(settings, 'CAUSE_SERVICE_URL', 'http://localhost:8001/causes')
    url = f"{cause_service_url}/details/{value}/"
    headers = {}
    if request and hasattr(request, 'headers'):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            headers['Authorization'] = auth_header
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise serializers.ValidationError('Cause service is not reachable.')
        cause_data = response.json()
        if 'id' in cause_data:
            return value
        else:
            raise serializers.ValidationError('Cause is not valid.')
    except requests.RequestException:
        raise serializers.ValidationError('Cause service is not reachable.')
    except Exception as e:
        raise serializers.ValidationError(f'An error occurred while validating cause: {str(e)}')


def get_user_email_from_service(user_id, request=None):
    """
    Get user email from user service.
    Returns email if found, raises exception if not.
    """
    user_service_url = getattr(settings, 'USER_SERVICE_URL', 'http://localhost:8000/user/auth')
    url = f"{user_service_url}/users/{user_id}/"
    headers = {}
    if request and hasattr(request, 'headers'):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            headers['Authorization'] = auth_header
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise ValueError('User not found in user service.')

        user_data = response.json()
        email = user_data.get('email')

        if not email:
            raise ValueError('User email not found in user service.')

        return email

    except requests.RequestException:
        raise ValueError('User service is not reachable.')
    except Exception as e:
        raise ValueError(f'Failed to get user email: {str(e)}')

def get_recipient_id_from_service(cause_id, request=None):
    cause_service_url = getattr(settings, 'CAUSE_SERVICE_URL', 'http://localhost:8001/causes')
    url = f"{cause_service_url}/details/{cause_id}/"
    headers = {}
    if request and hasattr(request, 'headers'):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            headers['Authorization'] = auth_header

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise ValueError(f'Failed to get {cause_id} information')

        cause_data = response.json()
        recipient_id = cause_data.get('organizer_id')  # organizer_id is the recipient

        if not recipient_id:
            raise ValueError(f'Recipient not found for cause {cause_id}')
        return recipient_id

    except requests.RequestException:
        raise ValueError('Cause service is not reachable.')
    except Exception as e:
        return ValueError(f'Failed to get recipient information for cause {cause_id}: {str(e)}')

def validate_request(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            # You can add any additional validation here
            return view_func(request, *args, **kwargs)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return wrapper