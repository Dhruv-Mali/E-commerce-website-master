# Stripe Payment Integration Setup

## Quick Setup Steps

### 1. Get Stripe API Keys
1. Go to https://dashboard.stripe.com/register
2. Create a free account
3. Navigate to **Developers** → **API keys**
4. Copy your **Publishable key** (starts with `pk_test_`)
5. Copy your **Secret key** (starts with `sk_test_`)

### 2. Update .env File
Replace the placeholder keys in `.env`:
```env
STRIPE_PUBLIC_KEY=pk_test_YOUR_ACTUAL_KEY_HERE
STRIPE_SECRET_KEY=sk_test_YOUR_ACTUAL_KEY_HERE
```

### 3. Restart Server
```bash
python manage.py runserver
```

## Testing Payment

### Test Card Numbers
Use these cards in Stripe checkout:

| Card Number | Result |
|-------------|--------|
| 4242 4242 4242 4242 | Success |
| 4000 0000 0000 9995 | Declined |
| 4000 0025 0000 3155 | Requires authentication |

- **Expiry**: Any future date (e.g., 12/34)
- **CVC**: Any 3 digits (e.g., 123)
- **ZIP**: Any 5 digits (e.g., 12345)

## How It Works

1. User fills checkout form
2. Clicks "Pay with Stripe"
3. Order saved to database
4. Redirects to Stripe payment page
5. After payment → redirects to success page
6. Stock automatically reduced

## Troubleshooting

**Error: "Invalid Stripe API keys"**
- Update `.env` with real keys from Stripe dashboard
- Restart Django server

**Error: "No such customer"**
- Normal in test mode, payment still works

**Payment page doesn't load**
- Check internet connection
- Verify Stripe keys are correct
- Check browser console for errors

## Production Setup

For live payments:
1. Complete Stripe account verification
2. Get live API keys (start with `pk_live_` and `sk_live_`)
3. Update `.env` with live keys
4. Set `DEBUG=False` in `.env`
5. Use HTTPS domain for success/cancel URLs
