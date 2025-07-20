from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken


def extract_user_from_token(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return Response(
                    {"error": "Authorization header is missing or invalid"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            token = auth_header.split(' ')[1]
            decoded_token = AccessToken(token)
            request.user_id = decoded_token['user_id']
            return view_func(request, *args, **kwargs)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return wrapper