from django.urls import path
from .views import signup, login, search_user, send_friend_request, send_friend_request, respond_friend_request, friend_list, pending_requests,all_friend_requests

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('search/', search_user, name='search_users'),
    path('send_friend_request/', send_friend_request, name='send_friend_request'),
    path('respond_friend_request/', respond_friend_request, name='respond_friend_request'),
    path('friend_list/', friend_list, name='friend_list'),
    path('pending_requests/', pending_requests, name='pending_requests'),
    path('all_friend_requests/', all_friend_requests, name='all_friend_requests'),
]
