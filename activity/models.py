from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ActivityLog(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="activities")
  activity_name = models.CharField(max_length=100)# e.g., "coding", "meeting"
  duration = models.IntegerField()#in minutes
  timestamp = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=20, default="active")

  def __str__(self):
    return f"{self.user.username} - {self.activity_name} ({self.duration}mins) "

