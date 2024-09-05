from django.shortcuts import render
from users.models import CustomUser
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from .models import FriendRequest
from rest_framework import generics, status
from .serializers import FriendRequestSerializer

# Create your views here.
class FriendRequestThrottle(UserRateThrottle):
    rate = '3/minute'

class SendFriendRequestView(APIView):
    throttle_classes = [FriendRequestThrottle]

    def post(self, request, *args, **kwargs):
        sender = request.user
        receiver_id = request.data.get('receiver_id')
        try:
            receiver = CustomUser.objects.get(id=receiver_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "Receiver not found"}, status=status.HTTP_404_NOT_FOUND)

        if sender == receiver:
            return Response({"error": "You cannot send a friend request to yourself"}, status=status.HTTP_400_BAD_REQUEST)

        friend_request, created = FriendRequest.objects.get_or_create(sender=sender, receiver=receiver)
        if created:
            return Response({"message": "Friend request sent!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Friend request already exists!"}, status=status.HTTP_400_BAD_REQUEST)

class RespondToFriendRequestView(APIView):
    def post(self, request, *args, **kwargs):
        request_id = request.data.get('request_id')
        action = request.data.get('action')

        try:
            friend_request = FriendRequest.objects.get(id=request_id, receiver=request.user)
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

        if action == 'accept':
            friend_request.status = 'accepted'
            friend_request.save()
            return Response({"message": "Friend request accepted!"})
        elif action == 'reject':
            friend_request.status = 'rejected'
            friend_request.save()
            return Response({"message": "Friend request rejected!"})
        else:
            return Response({"error": "Invalid action!"}, status=status.HTTP_400_BAD_REQUEST)

class ListPendingRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.objects.filter(receiver=self.request.user, status='pending')

