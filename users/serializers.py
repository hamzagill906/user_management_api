from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        # Add extra claims like user role etc.
        data['user_id'] = user.id
        data['role'] = user.role
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'profile_picture']  
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}  
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)  
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)

        instance.save()
        return instance

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'profile_picture']
        extra_kwargs = {'role': {'read_only': True}}