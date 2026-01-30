# ✅ COMPLETE FEATURE TESTING CHECKLIST

## Run Server First
```bash
python manage.py runserver
```

---

## 1. DATABASE & BACKEND TESTS

### Check Database Tables
```bash
python manage.py shell
```
```python
from apps.store.models_extended import *
from apps.store.models import *

# Check all tables exist
print("Products:", Product.objects.count())
print("Reviews:", ProductReview.objects.count())
print("Wishlist:", Wishlist.objects.count())
print("Coupons:", Coupon.objects.count())
print("Newsletter:", Newsletter.objects.count())
print("Recently Viewed:", RecentlyViewed.objects.count())
```

**Expected:** All commands work without errors

---

## 2. ADMIN PANEL TESTS

### Access Admin
1. Go to: http://127.0.0.1:8000/admin/
2. Login: admin / admin123

### Check Models Visible
- [ ] Products
- [ ] Customers
- [ ] Orders
- [ ] Product Reviews
- [ ] Wishlists
- [ ] Coupons
- [ ] Newsletter Subscribers
- [ ] Recently Viewed

**Expected:** All 8 models visible in admin

---

## 3. FRONTEND - PRODUCT REVIEWS

### Test Reviews
1. Go to: http://127.0.0.1:8000/store/
2. Click any product
3. Scroll down to "Customer Reviews" section
4. Check you see:
   - [ ] Review form with rating dropdown
   - [ ] Comment textarea
   - [ ] Submit button

### Submit Review (Logged In)
1. Login first: http://127.0.0.1:8000/l/
2. Go to product page
3. Select rating (1-5 stars)
4. Write comment
5. Click "Submit Review"

**Expected:** Success message appears

### Verify in Admin
1. Go to admin panel
2. Click "Product Reviews"
3. Check your review appears

**Expected:** Review visible with rating & comment

---

## 4. FRONTEND - WISHLIST

### Test Wishlist Button
1. Login: http://127.0.0.1:8000/l/
2. Go to any product page
3. Check you see:
   - [ ] "Wishlist" button with heart icon
   - [ ] Button next to "Add to Cart"

### Add to Wishlist
1. Click "Wishlist" button
2. Button should change to "In Wishlist"

**Expected:** Button changes color/text

### View Wishlist Page
1. Go to: http://127.0.0.1:8000/wishlist/
2. Check you see:
   - [ ] Product cards in grid
   - [ ] Product images
   - [ ] Remove button
   - [ ] View button

**Expected:** Your wishlist items displayed

### Verify in Admin
1. Go to admin panel
2. Click "Wishlists"
3. Check your wishlist entry

**Expected:** Wishlist entry visible

---

## 5. FRONTEND - NEWSLETTER

### Test Newsletter Form
1. Go to any page
2. Scroll to footer
3. Check you see:
   - [ ] "Subscribe to Newsletter" heading
   - [ ] Email input field
   - [ ] Subscribe button

### Subscribe
1. Enter email: test@example.com
2. Click "Subscribe"
3. Check for success message

**Expected:** Green checkmark with success message

### Verify in Admin
1. Go to admin panel
2. Click "Newsletter"
3. Check email appears

**Expected:** Email in newsletter list

---

## 6. FRONTEND - COUPONS (Admin Only)

### Create Coupon
1. Go to admin panel
2. Click "Coupons"
3. Click "Add Coupon"
4. Fill:
   - Code: SAVE10
   - Discount: 10%
   - Valid from: Today
   - Valid to: Next month
5. Save

**Expected:** Coupon created successfully

---

## 7. FRONTEND - RECENTLY VIEWED

### Auto-Track Views
1. Visit 3-4 different products
2. Go to admin panel
3. Click "Recently Viewed"

**Expected:** Your viewed products listed

---

## 8. API ENDPOINTS TEST

### Test Review API
Open browser console (F12) on product page:
```javascript
fetch('/api/add-review/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.cookie.match(/csrftoken=([^;]+)/)[1]
    },
    body: JSON.stringify({
        product_id: 1,
        rating: 5,
        comment: 'API Test'
    })
}).then(r => r.json()).then(console.log)
```

**Expected:** {success: true}

### Test Wishlist API
```javascript
fetch('/api/toggle-wishlist/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.cookie.match(/csrftoken=([^;]+)/)[1]
    },
    body: JSON.stringify({product_id: 1})
}).then(r => r.json()).then(console.log)
```

**Expected:** {success: true, action: 'added' or 'removed'}

### Test Newsletter API
```javascript
fetch('/api/subscribe-newsletter/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.cookie.match(/csrftoken=([^;]+)/)[1]
    },
    body: JSON.stringify({email: 'api@test.com'})
}).then(r => r.json()).then(console.log)
```

**Expected:** {success: true}

---

## 9. INTEGRATION TEST

### Complete User Flow
1. Register new user
2. Browse products
3. View product details
4. Add to wishlist
5. Write review
6. Add to cart
7. Checkout
8. View order history
9. Subscribe to newsletter

**Expected:** All steps work without errors

---

## ✅ FINAL CHECKLIST

- [ ] All database tables exist
- [ ] All models in admin panel
- [ ] Reviews form visible on product page
- [ ] Reviews can be submitted
- [ ] Wishlist button visible
- [ ] Wishlist page works
- [ ] Newsletter form in footer
- [ ] Newsletter subscription works
- [ ] Coupons can be created
- [ ] Recently viewed tracks products
- [ ] All API endpoints respond
- [ ] Complete user flow works

---

## 🎯 SUCCESS CRITERIA

**PASS:** All checkboxes checked
**FAIL:** Any checkbox unchecked

---

## 📊 EXPECTED RESULTS

### Frontend Visible:
✅ Product Reviews (on product page)
✅ Wishlist Button (on product page)
✅ Wishlist Page (/wishlist/)
✅ Newsletter Form (footer)

### Backend Visible:
✅ All models in admin
✅ API endpoints working
✅ Data saving correctly

### Integration:
✅ Frontend → API → Database → Admin
✅ All features connected properly

---

**If all tests pass: PROJECT IS 100% WORKING!** 🎉
