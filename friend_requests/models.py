from django.db import models
from users.models import CustomUser
# Create your models here.
class FriendRequest(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_friend_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_friend_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')), default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FriendRequest(from: {self.sender.email}, to: {self.receiver.email}, status: {self.status})"
    
    class Meta:
        db_table = 'friend_requests'