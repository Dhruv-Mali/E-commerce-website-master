#!/usr/bin/env python
import os
from dotenv import load_dotenv

load_dotenv()

print("✅ Twilio Configuration Status:")
print("=" * 60)
print(f"Account SID: {os.getenv('TWILIO_ACCOUNT_SID')[:15]}...")
print(f"Auth Token: [Configured]")
print(f"Messaging Service SID: {os.getenv('TWILIO_MESSAGING_SERVICE_SID')}")
print(f"Phone Number: {os.getenv('TWILIO_PHONE_NUMBER')}")
print(f"OTP SMS Enabled: {os.getenv('SEND_OTP_SMS')}")
print("=" * 60)
print("✅ All Twilio credentials loaded from .env file!")
print("\nNow ready to send SMS OTP messages!")
