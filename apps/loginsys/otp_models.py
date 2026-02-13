from django.db import models
from django.contrib.auth.models import User
import random
import string
from datetime import timedelta
from django.utils import timezone

class UserPhone(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='phone_profile')
    phone_number = models.CharField(max_length=20, unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"

    class Meta:
        verbose_name = "User Phone"
        verbose_name_plural = "User Phones"


class OTP(models.Model):
    OTP_TYPE_LOGIN = 'login'
    OTP_TYPE_VERIFICATION = 'verification'
    OTP_TYPE_CHOICES = [
        (OTP_TYPE_LOGIN, 'Login OTP'),
        (OTP_TYPE_VERIFICATION, 'Verification OTP'),
    ]

    phone_number = models.CharField(max_length=20)
    otp_code = models.CharField(max_length=6)
    otp_type = models.CharField(max_length=20, choices=OTP_TYPE_CHOICES, default=OTP_TYPE_LOGIN)
    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            # OTP valid for 10 minutes
            self.expires_at = timezone.now() + timedelta(minutes=10)
        if not self.otp_code:
            # Generate 6-digit OTP
            self.otp_code = ''.join(random.choices(string.digits, k=6))
        super().save(*args, **kwargs)

    def is_valid(self):
        """Check if OTP is still valid (not expired)"""
        return timezone.now() <= self.expires_at and not self.is_verified

    def is_expired(self):
        """Check if OTP has expired"""
        return timezone.now() > self.expires_at

    def verify(self, otp_code):
        """Verify OTP code"""
        self.attempts += 1
        
        if self.attempts > 5:
            return False, "Too many attempts. Please request a new OTP."
        
        if self.is_expired():
            return False, "OTP has expired. Please request a new OTP."
        
        if self.is_verified:
            return False, "OTP already used."
        
        if self.otp_code == otp_code:
            self.is_verified = True
            self.save()
            return True, "OTP verified successfully!"
        
        self.save()
        return False, f"Invalid OTP. {5 - self.attempts} attempts remaining."

    def __str__(self):
        return f"OTP for {self.phone_number} - {self.otp_type}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"
