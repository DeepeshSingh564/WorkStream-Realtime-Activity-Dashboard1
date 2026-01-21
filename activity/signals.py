# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import ActivityLog
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# import json


# @receiver(post_save, sender=ActivityLog)
# def broadcast_activity(sender, instance, created, **kwargs):
#   if created:
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#       "activities",{
#         "type":"activity_message",
#         "message": f"{instance.user.username} did {instance.activity_name} ({instance.duration} mins)"
#       }
#     )