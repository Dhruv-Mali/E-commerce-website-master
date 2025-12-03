# ⚡ Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Setup Stripe (2 minutes)
1. Go to https://dashboard.stripe.com/register
2. Copy your test keys
3. Update `.env`:
```env
STRIPE_PUBLIC_KEY=pk_test_YOUR_KEY
STRIPE_SECRET_KEY=sk_test_YOUR_KEY
```

### Step 2: Run Test (30 seconds)
```bash
python test_ecommerce.py
```
Should show: `Passed: 5/5`

### Step 3: Start Server (30 seconds)
```bash
python manage.py runserver
```

### Step 4: Test Purchase (2 minutes)
1. Visit: http://127.0.0.1:8000
2. Click "Store"
3. Add product to cart
4. Checkout
5. Use card: `4242 4242 4242 4242`
6. Complete payment
7. See success page ✅

---

## 🎯 URLs

| Page | URL |
|------|-----|
| Home | http://127.0.0.1:8000 |
| Store | http://127.0.0.1:8000/store/ |
| Cart | http://127.0.0.1:8000/cart/ |
| Admin | http://127.0.0.1:8000/admin/ |

---

## 💳 Test Cards

| Card | Result |
|------|--------|
| 4242 4242 4242 4242 | ✅ Success |
| 4000 0000 0000 9995 | ❌ Declined |

**Expiry:** Any future date (12/34)  
**CVC:** Any 3 digits (123)

---

## 🐛 Quick Fixes

**Payment not working?**
→ Check Stripe keys in `.env`

**Cart not updating?**
→ Clear browser cookies

**Database error?**
→ Run: `python manage.py migrate`

**Static files missing?**
→ Run: `python manage.py collectstatic`

---

## 📚 Full Documentation

- `ALL_FIXES_SUMMARY.md` - What was fixed
- `COMPLETE_SETUP_GUIDE.md` - Detailed setup
- `STRIPE_SETUP.md` - Stripe configuration

---

## ✅ Working Features

✅ Browse products  
✅ Search & filter  
✅ Add to cart  
✅ Update quantities  
✅ Secure checkout  
✅ Stripe payment  
✅ Order confirmation  
✅ Order history  
✅ Admin panel  
✅ Stock management  

---

**🎉 You're all set! Start selling!**
