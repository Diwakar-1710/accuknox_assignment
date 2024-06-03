from functools import wraps
from rest_framework_simplejwt.tokens import AccessToken
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()

def jwt_authentication(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Authorization header missing or invalid'}, status=401)

        token = auth_header.split(' ')[1]
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            request.user = User.objects.get(id=user_id)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=401)

        return view_func(request, *args, **kwargs)
    return _wrapped_view
