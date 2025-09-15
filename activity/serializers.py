from rest_framework import serializers
from .models import ActivityLog


class ActivityLogSerializer(serializers.ModelSerializer):
  user = serializers.StringRelatedField(read_only=True) #<- shows username, but not writable
  
  class Meta:
    model = ActivityLog
    fields = ['id', 'user', 'activity_name', 'duration', 'timestamp', 'status']