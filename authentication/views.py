from .serializers import UserSerializer, EmailVerificationSerializer
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status, views
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from django.conf import settings
from django.urls import reverse
from drf_yasg import openapi
from .models import User
from .utils import Util
import jwt


from django.contrib.sites.shortcuts import get_current_site

class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        user = request.data
        serializer = self.get_serializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request)
        relativeLink = reverse('verify-email')

        absurl = 'http://' + str(current_site) + relativeLink + "?token=" + str(token)

        email_body = 'Hi ' + user.username + ' Use the link below to verify your email:\n' + absurl
        data = {'email_body': email_body, 'to_email': user.email, "email_subject": "Verify your Email"}
        Util.send_email(data)

        return Response({"status": "success", "message": "User created successfully.", "data": user_data},
                        status=status.HTTP_201_CREATED)




class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description="description", type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload =  jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({"Email": "Successfully activated"},status=status.HTTP_200_OK)
        
        except jwt.ExpiredSignatureError as identifir:
            return Response({"Error": "Activation Link Expired"},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifir:
            return Response({"Error": "Invalid Token"},status=status.HTTP_400_BAD_REQUEST)