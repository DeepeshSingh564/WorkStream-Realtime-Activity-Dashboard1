from django.urls import path
from . import views

urlpatterns=[
  path('', views.home , name="home"),
  path('signup/', views.signup_page, name='signup_page'),
  path('login/', views.login_page, name='login_page'),
  # path("auth/", auth_page, name="auth_page" ),#frontend auth page
]