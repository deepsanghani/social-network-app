from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4
from datetime import timedelta
from django.utils import timezone

def default_expiry_time():
    return timezone.now() + timedelta(hours=1)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    token = models.UUIDField(default=uuid4, editable=False, unique=True)
    expiry_time = models.DateTimeField(default=default_expiry_time)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    def refresh_token(self):
        """Refreshes the token and updates the expiry time."""
        self.token = uuid4()
        self.expiry_time = default_expiry_time()
        self.save()

    def is_token_expired(self):
        """Checks if the token is expired."""
        return timezone.now() > self.expiry_time
    
    class Meta:
        db_table = 'users'
    
    @property
    def friends(self):
        sent_friend_requests = self.sent_friend_requests.filter(status='accepted').values_list('receiver', flat=True)
        received_friend_requests = self.received_friend_requests.filter(status='accepted').values_list('sender', flat=True)
        friend_ids = list(sent_friend_requests) + list(received_friend_requests)
        return CustomUser.objects.filter(id__in=friend_ids)

