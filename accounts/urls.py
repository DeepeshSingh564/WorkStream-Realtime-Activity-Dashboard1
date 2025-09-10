from django.urls import path
from . import views
from .views import  SignUpView, LoginView, LogoutView, signup_page


urlpatterns=[
  path('', views.home , name="home"),
  path('signup/', views.signup_page, name='signup_page'),
  path('login/', views.login_page, name='login_page'),
  # path("auth/", auth_page, name="auth_page" ),#frontend auth page
  path('api/signup/', SignUpView.as_view(), name='api_signup'),
  path('api/login/', LoginView.as_view(), name='api_login'),
  path('api/logout/', LogoutView.as_view(), name='api_logout'),
]