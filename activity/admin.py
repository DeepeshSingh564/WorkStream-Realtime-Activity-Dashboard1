from django.contrib import admin
from .models import ActivityLog
# Register your models here.

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_name', 'duration', 'timestamp')
    list_filter = ('activity_name', 'timestamp')
    search_fields = ('activity_name', 'user__username')
