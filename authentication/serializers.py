from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68,
                                     min_length=8,
                                     write_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
    
    # built in method
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        
        if not username.isalnum():
            raise serializers.ValidationError("Username must be alphanumeric")
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)




class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    class Meta:
        model = User
        fields = ['token']
        



class LogInSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    username = serializers.CharField(min_length=4, max_length=100, read_only=True)
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    tokens = serializers.CharField(max_length=150, read_only=True)
    
    class Meta:
        model = User
        fields = ['email','password', 'username', 'tokens']
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        
        user = auth.authenticate(email=email, password=password)
        
        if not user:
            raise AuthenticationFailed('Invalid Credentials, Please Try Again')
        if not user.is_verified:
            raise AuthenticationFailed('Please Verify Your Account First')
        if not user.is_active:
            raise AuthenticationFailed("User is InActive")
        
        return {
            'email':user.email,
            'username':user.username,
            'tokens':user.tokens,
        }
            
        return super().validate(attrs)
    

        