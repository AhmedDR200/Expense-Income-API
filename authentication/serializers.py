from rest_framework import serializers
from .models import User




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
