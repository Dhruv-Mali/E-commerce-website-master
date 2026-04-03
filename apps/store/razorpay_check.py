"""
Test script to verify Razorpay integration
Run: python manage.py shell < apps/store/test_razorpay.py
"""

import razorpay
from django.conf import settings

print("\n" + "="*60)
print("RAZORPAY INTEGRATION TEST")
print("="*60)

# Test 1: Check credentials are loaded
print("\n[1] Checking Razorpay Credentials...")
key_id = settings.RAZORPAY_KEY_ID
key_secret = settings.RAZORPAY_KEY_SECRET

if not key_id or not key_secret:
    print("✗ FAILED: Credentials not loaded from .env")
    print(f"  KEY_ID: {key_id}")
    print(f"  KEY_SECRET: {key_secret}")
    print("\nFix: Update .env file with valid Razorpay test keys")
else:
    print(f"✓ PASSED: Credentials loaded")
    print(f"  KEY_ID: {key_id[:20]}...")
    print(f"  KEY_SECRET: {key_secret[:20]}...")

# Test 2: Initialize Razorpay client
print("\n[2] Initializing Razorpay Client...")
try:
    client = razorpay.Client(auth=(key_id, key_secret))
    print("✓ PASSED: Razorpay client initialized")
except Exception as e:
    print(f"✗ FAILED: {str(e)}")
    exit(1)

# Test 3: Create test order
print("\n[3] Creating Test Order...")
try:
    order_data = {
        'amount': 50000,  # ₹500 in paise
        'currency': 'INR',
        'payment_capture': 1
    }
    order = client.order.create(data=order_data)
    print("✓ PASSED: Test order created")
    print(f"  Order ID: {order['id']}")
    print(f"  Amount: ₹{order['amount']/100}")
    print(f"  Status: {order['status']}")
except Exception as e:
    print(f"✗ FAILED: {str(e)}")
    print("\nPossible causes:")
    print("  - Invalid API keys")
    print("  - Network connectivity issue")
    print("  - Razorpay account not verified")
    exit(1)

# Test 4: Verify order details
print("\n[4] Verifying Order Details...")
try:
    verified_order = client.order.fetch(order['id'])
    if verified_order['id'] == order['id']:
        print("✓ PASSED: Order verified")
        print(f"  Order ID: {verified_order['id']}")
        print(f"  Amount: ₹{verified_order['amount']/100}")
    else:
        print("✗ FAILED: Order verification mismatch")
except Exception as e:
    print(f"✗ FAILED: {str(e)}")
    exit(1)

print("\n" + "="*60)
print("✓ ALL TESTS PASSED - Razorpay integration is working!")
print("="*60)
print("\nNext steps:")
print("1. Go to http://127.0.0.1:8000/store/")
print("2. Add items to cart")
print("3. Go to checkout")
print("4. Fill form and click 'Proceed to Payment'")
print("5. Use test card: 4111 1111 1111 1111")
print("6. Use any future expiry and CVV")
print("\n")
