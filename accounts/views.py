from django.http import request
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .serializers import UserSignUpSerializer, UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def home(request):
  return render(request , "accounts/home.html")


def signup_page(request):
  return render(request, "accounts/signup.html")

def login_page(request):
  return render(request, "accounts/login.html")



# def auth_page(request):
#   return render(request, "accounts/auth.html")

class SignUpView(APIView):
  authentication_classes = []  # No authentication needed for signup
  permission_classes = [AllowAny]  # Allow anyone to sign up
  
  def post(self, request):
    serializer = UserSignUpSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      token, _ = Token.objects.get_or_create(user=user)
      return Response({"token": token.key, "username": user.username})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
  authentication_classes = []  # No authentication needed for login
  permission_classes = [AllowAny]  # Allow anyone to login
  
  def post(self, request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
      user = authenticate(
        username = serializer.validated_data['username'],
        password = serializer.validated_data['password']
      )
      if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "username": user.username})

      return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
  authentication_classes = [TokenAuthentication]

  def post(self, request):
    request.user.auth_token.delete()
    return Response({"message":"Logged out successfully"})