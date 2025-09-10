from django.urls import path
from .import views
from .views import ActivityLogListCreateView, ActivityLogDetailView
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns=[
  # path('', views.index, name='index'),
  path('activities/', ActivityLogListCreateView.as_view(),name='activity-list'),
  path('activities/<int:pk>/', ActivityLogDetailView.as_view(),name='activity-detail'),
  path("test/", views.activity_test, name="activity_test"),
  path("dashboard/", views.activity_dashboard, name="activity_dashboard"),
  path("token/", obtain_auth_token, name="api_token")
]