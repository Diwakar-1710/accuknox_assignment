from django.shortcuts import get_object_or_404
from rest_framework import status as drf_status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import SignupSerializer, LoginSerializer, FriendRequestSerializer, UserSerializer
from .models import FriendRequest
from .jwt_auth import jwt_authentication
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Signup successful'}, status=drf_status.HTTP_201_CREATED)
    return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'display_name': user.username, 
                'email_id': email,
                'password': password,
                'status': 'SUCCESS',
                'message': 'Login Successful',
                'token': str(refresh.access_token),
            }, status=drf_status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=drf_status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@jwt_authentication
def search_user(request):
    query = request.query_params.get('query', '')
    users = User.objects.filter(Q(email__icontains=query) | Q(username__icontains=query))
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=drf_status.HTTP_200_OK)

@api_view(['POST'])
@jwt_authentication
def send_friend_request(request):
    data = {'to_user': request.data.get('to_user')}
    serializer = FriendRequestSerializer(data=data, context={'request': request})
    print('serializer---->',serializer)
    if serializer.is_valid():
        now = timezone.now()
        one_minute_ago = now - timedelta(minutes=1)
        recent_requests_count = FriendRequest.objects.filter(
            from_user=request.user,
            timestamp__gte=one_minute_ago
        ).count()

        if recent_requests_count >= 3:
            return Response(
                {'error': 'You have sent too many friend requests in the last minute. Please try again later.'},
                status=drf_status.HTTP_429_TOO_MANY_REQUESTS
            )

        serializer.save()
        to_user = serializer.validated_data['to_user']
        return Response({'message': 'Friend request sent',
                         'to_user': to_user.id}, status=drf_status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@jwt_authentication
def respond_friend_request(request):
    from_user_id = request.data.get('from_user')
    request_status = request.data.get('status')  # Rename status variable to request_status

    if not from_user_id:
        return Response({'error': 'from_user is required'}, status=drf_status.HTTP_400_BAD_REQUEST)
    if request_status not in ['accepted', 'rejected']:
        return Response({'error': 'Invalid status'}, status=drf_status.HTTP_400_BAD_REQUEST)

    from_user = get_object_or_404(User, id=from_user_id)
    friend_request = get_object_or_404(FriendRequest, from_user=from_user, to_user=request.user)

    friend_request.status = request_status
    friend_request.save()

    message = 'Friend request accepted' if request_status == 'accepted' else 'Friend request rejected'
    return Response({'message': message}, status=drf_status.HTTP_200_OK)

@api_view(['GET'])
@jwt_authentication
def friend_list(request):
    friends = User.objects.filter(
        Q(sent_requests__status='accepted', sent_requests__to_user=request.user) |
        Q(received_requests__status='accepted', received_requests__from_user=request.user)
    )
    serializer = UserSerializer(friends, many=True)
    return Response(serializer.data, status=drf_status.HTTP_200_OK)

@api_view(['GET'])
@jwt_authentication
def pending_requests(request):
    print(request.user)
    requests = FriendRequest.objects.filter(from_user=request.user, status='pending')
    serializer = FriendRequestSerializer(requests, many=True)
    return Response(serializer.data, status=drf_status.HTTP_200_OK)

@api_view(['GET'])
@jwt_authentication
def all_friend_requests(request):
    requests = FriendRequest.objects.all()
    serializer = FriendRequestSerializer(requests, many=True)
    return Response(serializer.data, status=drf_status.HTTP_200_OK)
