from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import CustomUser,UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'address', 'latitude', 'longitude']

class CustomUserCreateSerializer(UserCreateSerializer):
   class Meta(UserCreateSerializer.Meta):
       model = CustomUser
       fields = ('id', 'first_name', 'last_name', 'phone_number', 'role', 'email', 'password')

class CustomUserSerializer(UserSerializer):
    profile = UserProfileSerializer(read_only=True)
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'role', 'email', 'profile')