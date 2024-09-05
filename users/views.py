from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django.db.models import Q
from .models import CustomUser
from .serializers import UserSerializer
from django.contrib.auth import authenticate
import uuid
from datetime import timedelta
from django.utils import timezone

class SignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            unique_token = uuid.uuid4()
            while CustomUser.objects.filter(token=unique_token).exists():
                unique_token = uuid.uuid4()
            
            user.token = unique_token
            user.expiry_time = timezone.now() + timedelta(hours=1)
            user.save()
            return Response({"token": str(user.token)}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email', 'username']

    def get_queryset(self):
        query = self.request.query_params.get('search', '')
        return CustomUser.objects.filter(
            Q(email__iexact=query) | Q(username__icontains=query)
        )

class ListFriendsView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.request.user.friends.all()
