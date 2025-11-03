# 💳 Stripe Payment Integration Guide

Complete guide to integrate Stripe payment gateway in your Django e-commerce application.

---

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Get Stripe API Keys](#get-stripe-api-keys)
3. [Configuration](#configuration)
4. [How It Works](#how-it-works)
5. [Testing](#testing)
6. [Production Setup](#production-setup)

---

## Prerequisites

- Stripe account (free to create)
- Python Stripe library installed (`pip install stripe==5.4.0`)
- Django project setup

---

## Get Stripe API Keys

### Step 1: Create Stripe Account
1. Go to [https://stripe.com](https://stripe.com)
2. Click "Sign up" and create your account
3. Complete email verification

### Step 2: Get API Keys
1. Login to Stripe Dashboard
2. Click "Developers" in the top menu
3. Click "API keys" in the left sidebar
4. You'll see two keys:
   - **Publishable key** (starts with `pk_test_`)
   - **Secret key** (starts with `sk_test_`)

### Step 3: Copy Keys
```
Publishable key: pk_test_51xxxxxxxxxxxxxxxxxxxxx
Secret key: sk_test_51xxxxxxxxxxxxxxxxxxxxx
```

---

## Configuration

### 1. Update .env File
```env
SECRET_KEY=your_django_secret_key
STRIPE_PUBLIC_KEY=pk_test_51xxxxxxxxxxxxxxxxxxxxx
STRIPE_SECRET_KEY=sk_test_51xxxxxxxxxxxxxxxxxxxxx
DEBUG=True
```

### 2. Settings Configuration (Already Done)
In `ecommerce/settings.py`:
```python
import os

STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
```

### 3. Initialize Stripe in Views (Already Done)
In `store/views.py`:
```python
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
```

---

## How It Works

### Payment Flow

1. **User adds items to cart**
   - Items stored in database (logged-in users)
   - Items stored in cookies (guest users)

2. **User proceeds to checkout**
   - Clicks "Make Payment" button
   - System calculates total amount

3. **Stripe Checkout Session Created**
   - Backend creates Stripe product
   - Creates price object
   - Generates checkout session URL

4. **User redirected to Stripe**
   - Secure Stripe-hosted payment page
   - User enters card details
   - Stripe processes payment

5. **Payment Success/Failure**
   - Success: Redirect to homepage
   - Failure: Redirect to cancelled page

### Code Implementation

**In `store/utils.py`:**
```python
def product_sales_pipeline(product_name, product_price):
    # Create Stripe product
    stripe_product = stripe.Product.create(name=str(product_name))
    
    # Create price (amount in smallest currency unit)
    stripe_price = stripe.Price.create(
        product=stripe_product.id,
        unit_amount=int(product_price),  # Amount in paise (₹1 = 100 paise)
        currency='inr'
    )
    
    # Create checkout session
    checkout_session = stripe.checkout.Session.create(
        line_items=[{
            'price': stripe_price.id,
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/',
        cancel_url='http://127.0.0.1:8000/payments/cancelled/'
    )
    
    return checkout_session.url
```

**In `store/views.py`:**
```python
def checkout(request):
    if request.POST.get('make-payment-btn'):
        # Get order details
        order = get_order()
        
        # Create Stripe checkout
        stripe_url = product_sales_pipeline(
            order.id, 
            order.get_cart_total * 100  # Convert to paise
        )
        
        # Redirect to Stripe
        return HttpResponseRedirect(stripe_url)
```

---

## Testing

### Test Card Numbers

Stripe provides test cards for development:

| Card Number | Description |
|-------------|-------------|
| 4242 4242 4242 4242 | Success |
| 4000 0000 0000 0002 | Card declined |
| 4000 0000 0000 9995 | Insufficient funds |

**Test Card Details:**
- **Expiry Date:** Any future date (e.g., 12/25)
- **CVC:** Any 3 digits (e.g., 123)
- **ZIP:** Any 5 digits (e.g., 12345)

### Testing Steps

1. Start your Django server:
   ```bash
   python manage.py runserver
   ```

2. Add products to cart

3. Go to checkout page

4. Click "Make Payment"

5. Use test card: `4242 4242 4242 4242`

6. Complete payment

7. Check Stripe Dashboard → Payments to see test transaction

---

## Production Setup

### 1. Switch to Live Keys

1. Go to Stripe Dashboard
2. Toggle from "Test mode" to "Live mode"
3. Get live API keys (start with `pk_live_` and `sk_live_`)
4. Update `.env` file:
   ```env
   STRIPE_PUBLIC_KEY=pk_live_xxxxxxxxxxxxx
   STRIPE_SECRET_KEY=sk_live_xxxxxxxxxxxxx
   ```

### 2. Update URLs

In `store/utils.py`, change URLs to production:
```python
base_endpoint = 'https://yourdomain.com'
success_url = f"{base_endpoint}/"
cancel_url = f"{base_endpoint}/payments/cancelled/"
```

### 3. Enable Webhooks (Optional)

For advanced features like payment confirmation:

1. Go to Stripe Dashboard → Developers → Webhooks
2. Add endpoint: `https://yourdomain.com/webhook/stripe/`
3. Select events: `checkout.session.completed`
4. Copy webhook secret
5. Add to `.env`:
   ```env
   STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
   ```

---

## Currency Support

Current setup uses INR (Indian Rupees). To change currency:

```python
stripe_price = stripe.Price.create(
    product=stripe_product.id,
    unit_amount=int(product_price),
    currency='usd'  # Change to: usd, eur, gbp, etc.
)
```

**Note:** Amount must be in smallest currency unit:
- INR: ₹1 = 100 paise
- USD: $1 = 100 cents
- EUR: €1 = 100 cents

---

## Security Best Practices

1. ✅ Never expose secret key in frontend
2. ✅ Always use HTTPS in production
3. ✅ Store keys in environment variables
4. ✅ Use Stripe's hosted checkout (already implemented)
5. ✅ Validate amounts on server-side
6. ✅ Enable webhook signature verification

---

## Troubleshooting

### Issue: "Invalid API Key"
**Solution:** Check if keys are correctly set in `.env` file

### Issue: "Amount must be positive integer"
**Solution:** Ensure amount is multiplied by 100 (convert to paise/cents)

### Issue: "Redirect not working"
**Solution:** Check success_url and cancel_url are correct

### Issue: "Payment not processing"
**Solution:** Verify Stripe account is activated and not restricted

---

## Additional Resources

- [Stripe Documentation](https://stripe.com/docs)
- [Stripe API Reference](https://stripe.com/docs/api)
- [Stripe Testing Guide](https://stripe.com/docs/testing)
- [Stripe Dashboard](https://dashboard.stripe.com)

---

## Support

For Stripe-specific issues:
- Email: support@stripe.com
- Documentation: https://stripe.com/docs

For project issues:
- Open an issue on GitHub
- Email: dhruvmali9039@gmail.com

---

**🎉 Your Stripe integration is ready to use!**
