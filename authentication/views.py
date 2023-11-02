from rest_framework import generics
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


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




class VerifyEmail(generics.GenericAPIView):
    serializer_class = UserSerializer
    def get(self):
        pass