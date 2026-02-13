from django.urls import path

from . import views
from . import otp_views

urlpatterns = [
    path('', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('profile/', views.profile, name='profile'),
    
    # OTP Authentication Routes
    path('otp-login/', otp_views.otp_login, name='otp_login'),
    path('verify-otp/', otp_views.verify_otp, name='verify_otp'),
    path('resend-otp/', otp_views.resend_otp, name='resend_otp'),
]
