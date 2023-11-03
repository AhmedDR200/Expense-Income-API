from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
    path('verify-email/', views.VerifyEmail.as_view(), name='verify-email'),
    path('login/', views.LogInView.as_view(), name="login"),
]
