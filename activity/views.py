from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import ActivityLog
from .serializers import ActivityLogSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import sys


def activity_test(request):
    return render(request, "activity/test.html")


def activity_dashboard(request):
    return render(request, "activity/dashboard.html")


class ActivityLogListCreateView(generics.ListCreateAPIView):
    serializer_class = ActivityLogSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # ✅ Only return activities of logged-in user
        return ActivityLog.objects.filter(user=self.request.user).order_by('-timestamp')

    def perform_create(self, serializer):
        # ✅ Save activity for the logged-in user
        activity = serializer.save(user=self.request.user)
        serialized = ActivityLogSerializer(activity).data

        # Debug print
        print("Broadcasting (views.perform_create):", serialized, file=sys.stderr, flush=True)

        # Broadcast to WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{self.request.user.id}",  # ✅ per-user channel group
            {
                "type": "activity_message",
                "data": serialized
            }
        )


class ActivityLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivityLogSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # ✅ A user can only fetch/update/delete their own activities
        return ActivityLog.objects.filter(user=self.request.user)
