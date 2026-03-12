#!/usr/bin/env python
"""
Quick Razorpay Connection Test
Run this to verify your Razorpay credentials are working
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("RAZORPAY CONNECTION TEST")
print("=" * 60)

# Check if keys are loaded
key_id = os.getenv('RAZORPAY_KEY_ID')
key_secret = os.getenv('RAZORPAY_KEY_SECRET')

print(f"\n1. Checking .env file...")
print(f"   Key ID: {key_id}")
print(f"   Key Secret: {key_secret[:10] if key_secret else 'None'}...***")

if not key_id or key_id == 'rzp_test_XXXXXXXXXXXXXX':
    print("\n❌ ERROR: Razorpay Key ID is not set or is placeholder!")
    print("\nFIX:")
    print("1. Go to https://dashboard.razorpay.com/")
    print("2. Settings → API Keys → Generate Test Key")
    print("3. Copy Key ID and Key Secret")
    print("4. Update .env file with real values")
    print("5. Restart Django server")
    exit(1)

if not key_secret or key_secret == 'XXXXXXXXXXXXXXXXXXXXXXXX':
    print("\n❌ ERROR: Razorpay Key Secret is not set or is placeholder!")
    print("\nFIX: Update .env file with real Razorpay Key Secret")
    exit(1)

if not key_id.startswith('rzp_test_'):
    print("\n⚠️  WARNING: Key ID doesn't start with 'rzp_test_'")
    print("   Make sure you're using TEST keys, not LIVE keys!")

print("\n2. Testing Razorpay connection...")

try:
    import razorpay
    
    client = razorpay.Client(auth=(key_id, key_secret))
    
    # Try to create a test order
    test_order = client.order.create({
        'amount': 10000,  # ₹100 in paise
        'currency': 'INR',
        'payment_capture': 1
    })
    
    print(f"   ✅ Connection successful!")
    print(f"   Test Order ID: {test_order['id']}")
    print(f"   Amount: ₹{test_order['amount'] / 100}")
    print(f"   Currency: {test_order['currency']}")
    print(f"   Status: {test_order['status']}")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nYour Razorpay integration is working correctly.")
    print("You can now test payments in your application.")
    print("\nTest Card Details:")
    print("  Card Number: 4111 1111 1111 1111")
    print("  CVV: Any 3 digits")
    print("  Expiry: Any future date")
    
except razorpay.errors.BadRequestError as e:
    print(f"\n❌ Bad Request Error: {e}")
    print("\nPossible causes:")
    print("- Invalid API keys")
    print("- Keys don't match (test vs live)")
    print("- Account not activated")
    
except razorpay.errors.ServerError as e:
    print(f"\n❌ Server Error: {e}")
    print("\nRazorpay servers might be down. Try again later.")
    
except Exception as e:
    print(f"\n❌ Unexpected Error: {e}")
    print(f"\nError Type: {type(e).__name__}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
