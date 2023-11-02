from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.response import Response


class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer
    
    def post(self, request):
        user = request.data
        serializer = self.get_serializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        user_data = serializer.data
        return Response({"status": "success", "message": "User created successfully.", "data": user_data},
                        status=status.HTTP_201_CREATED)
        