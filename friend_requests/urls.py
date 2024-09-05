from django.contrib import admin
from django.urls import path, include
from friend_requests.views import ListPendingRequestsView, SendFriendRequestView, RespondToFriendRequestView

urlpatterns = [
    path('friend-requests/', ListPendingRequestsView.as_view(), name='pending_requests'),
    path('friend-request/send/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('friend-request/respond/', RespondToFriendRequestView.as_view(), name='respond_friend_request'),
]

