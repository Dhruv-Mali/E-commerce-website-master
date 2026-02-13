import requests
import os
from django.conf import settings

class OTPService:
    """Service to handle OTP sending via SMS"""
    
    # SMS Gateway Options:
    # 1. Twilio (Recommended) - twilio.com
    # 2. AWS SNS - aws.amazon.com/sns
    # 3. Nexmo/Vonage - vonage.com
    # 4. FastAPI/PlaySMS - free alternatives
    
    @staticmethod
    def send_otp_sms(phone_number, otp_code):
        """
        Send OTP via SMS
        
        This is a template for sending SMS using Twilio.
        To enable:
        1. Install: pip install twilio
        2. Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN in .env
        3. Set TWILIO_PHONE_NUMBER in .env
        """
        
        # Check if SMS sending is enabled
        send_sms = os.environ.get('SEND_OTP_SMS', 'False').lower() == 'true'
        
        if not send_sms:
            # For development: just return success
            # In production, set SEND_OTP_SMS=True in .env
            print(f"[DEV MODE] OTP {otp_code} for {phone_number}")
            return True, f"OTP: {otp_code}"
        
        try:
            # Twilio Configuration (add to .env)
            from twilio.rest import Client
            
            account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
            auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
            messaging_service_sid = os.environ.get('TWILIO_MESSAGING_SERVICE_SID')
            twilio_phone = os.environ.get('TWILIO_PHONE_NUMBER')
            
            if not all([account_sid, auth_token]):
                return False, "SMS gateway not configured"
            
            client = Client(account_sid, auth_token)
            
            # Use messaging service SID if available, otherwise use phone number
            if messaging_service_sid:
                message = client.messages.create(
                    messaging_service_sid=messaging_service_sid,
                    body=f"Your login OTP is: {otp_code}\nDo not share with anyone. Valid for 10 minutes.",
                    to=phone_number
                )
            else:
                if not twilio_phone:
                    return False, "Twilio phone number not configured"
                message = client.messages.create(
                    body=f"Your login OTP is: {otp_code}\nDo not share with anyone. Valid for 10 minutes.",
                    from_=twilio_phone,
                    to=phone_number
                )
            
            return True, f"OTP sent to {phone_number}"
        
        except Exception as e:
            print(f"SMS Error: {str(e)}")
            return False, f"Failed to send OTP: {str(e)}"
    
    @staticmethod
    def format_phone_number(phone_number):
        """
        Format phone number to international format
        Input: 9876543210 or 919876543210 or +919876543210
        Output: +919876543210
        """
        phone = phone_number.replace(' ', '').replace('-', '')
        
        if phone.startswith('+'):
            return phone
        elif phone.startswith('91'):
            return '+' + phone
        elif len(phone) == 10:
            return '+91' + phone
        else:
            return '+91' + phone[-10:]


class SMSGatewaySetup:
    """Setup guide for SMS gateways"""
    
    TWILIO_SETUP = """
    TWILIO SMS GATEWAY SETUP
    ========================
    
    1. Create Twilio Account:
       - Visit https://www.twilio.com/console
       - Sign up for free account (get $15 credit)
       - Verify phone number
    
    2. Get Credentials:
       - Account SID: Copy from Dashboard
       - Auth Token: Copy from Dashboard
       - Phone Number: Buy a Twilio number (free trial has limitations)
    
    3. Install SDK:
       pip install twilio
    
    4. Add to .env:
       TWILIO_ACCOUNT_SID=your_account_sid
       TWILIO_AUTH_TOKEN=your_auth_token
       TWILIO_PHONE_NUMBER=+1234567890
       SEND_OTP_SMS=True
    
    5. Test it:
       python manage.py shell
       from apps.loginsys.otp_service import OTPService
       OTPService.send_otp_sms('+919876543210', '123456')
    """
    
    AWS_SNS_SETUP = """
    AWS SNS SETUP
    =============
    
    1. Create AWS Account:
       - Visit https://aws.amazon.com
       - Sign up (free tier available)
    
    2. Setup SNS:
       - Go to AWS SNS Console
       - Create Topic
       - Create SMS subscription
    
    3. Install SDK:
       pip install boto3
    
    4. Add to .env:
       AWS_ACCESS_KEY_ID=your_key
       AWS_SECRET_ACCESS_KEY=your_secret
       AWS_SNS_TOPIC_ARN=arn:aws:sns:region:account:topic
       AWS_REGION=us-east-1
    """
    
    @staticmethod
    def print_setup_guide(gateway='TWILIO'):
        if gateway.upper() == 'TWILIO':
            print(SMSGatewaySetup.TWILIO_SETUP)
        elif gateway.upper() == 'AWS':
            print(SMSGatewaySetup.AWS_SNS_SETUP)
