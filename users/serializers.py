from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
  # campos read only
  username = serializers.CharField(source='user.username', read_only=True)
  email = serializers.EmailField(source='user.email', read_only=True)
  first_name = serializers.CharField(source='user.first_name', read_only=True)
  last_name = serializers.CharField(source='user.last_name', read_only=True)
  
  # campos editables
  birth_date = serializers.DateField(allow_null=True, required=False)
  height = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True, required=False)
  weight = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True, required=False)
  bio = serializers.CharField(max_length=500, allow_null=True, required=False, allow_blank=True)
  
  class Meta:
    model = Profile
    fields = ['username', 'email', 'first_name', 'last_name', 'birth_date', 'height', 'weight', 'bio']
  
  def update(self, instance, validated_data):
    instance.birth_date = validated_data.get('birth_date', instance.birth_date)
    instance.height = validated_data.get('height', instance.height)
    instance.weight = validated_data.get('weight', instance.weight)
    instance.bio = validated_data.get('bio', instance.bio)
    instance.save()
    return instance

class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)

  class Meta:
    model = User
    fields = ['username', 'email', 'password', 'first_name', 'last_name']
  
  def create(self, validated_data):
    password = validated_data.pop('password')
    user = User(**validated_data)
    user.set_password(password)
    user.save()

    Profile.objects.create(user=user)

    return user
