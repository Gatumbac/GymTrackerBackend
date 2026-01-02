from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserProfileSerializer
from .models import Profile

# Create your views here.

class RegisterView(generics.CreateAPIView):
  queryset = User.objects.all()
  permission_classes = [AllowAny]
  serializer_class = RegisterSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
  serializer_class = UserProfileSerializer
  permission_classes = [IsAuthenticated]
  
  def get_object(self):
    profile, created = Profile.objects.get_or_create(user=self.request.user)
    return profile