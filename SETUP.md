# ✅ Setup & Feature Guide

## 🚀 Quick Start (3 Commands)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit: http://localhost:8000/

---

## ✨ Features

1. **Product Catalog** - Browse, search, filter products with pagination
2. **Shopping Cart** - Cookie-based (guests) and database (authenticated users)
3. **Razorpay Payments** - Secure payment processing with signature verification
4. **Order Management** - Track orders with status updates
5. **PDF Invoices** - Downloadable invoices for completed orders
6. **Product Reviews & Ratings** - 1-5 star system with verified purchase badges
7. **Wishlist System** - Save products for later
8. **Newsletter Subscription** - Email subscription management
9. **Coupon System** - Discount codes with validation
10. **Recently Viewed** - Product browsing history
11. **Custom Admin Dashboard** - Staff-only product & order management
12. **Multilingual (i18n)** - English & Hindi language support
13. **Security Middleware** - Rate limiting, XSS/SQL injection protection
14. **Performance Caching** - Redis or local memory cache
15. **Comprehensive Logging** - Error tracking to `logs/ecommerce.log`

---

## 📁 Key Files

```
apps/store/
├── models.py              # Customer, Product, Order, OrderItem, ShippingAddress
├── models_extended.py     # ProductReview, Wishlist, Coupon, RecentlyViewed, Newsletter
├── views.py               # Main views (store, cart, checkout, admin, invoices)
├── api_views.py           # API endpoints (reviews, wishlist, newsletter)
├── admin.py               # Core Django admin config
├── admin_extended.py      # Extended models admin config
├── utils.py               # Razorpay payment utilities
├── cache.py               # Caching utilities
├── validators.py          # Input validation
├── security_middleware.py # Security middleware
├── logging_utils.py       # Logging helpers
└── tests.py               # Unit tests
```

---

## 🔌 API Endpoints

```javascript
// Add Review
POST /api/add-review/
{"product_id": 1, "rating": 5, "comment": "Great!"}

// Toggle Wishlist
POST /api/toggle-wishlist/
{"product_id": 1}

// Get Wishlist
GET /api/wishlist/

// Subscribe Newsletter
POST /api/subscribe-newsletter/
{"email": "user@example.com"}

// Download Invoice
GET /invoice/<order_id>/
```

---

## 🗄️ Database Models

### Core (models.py)
- `Customer` - User profile with name, email
- `Product` - Products with stock tracking, categories, views
- `Order` - Orders with Razorpay payment ID, status tracking
- `OrderItem` - Line items in orders
- `ShippingAddress` - Delivery addresses

### Extended (models_extended.py)
- `ProductReview` - Product reviews with 1-5 star ratings
- `Wishlist` - User wishlists
- `Coupon` - Discount coupons with validity period
- `RecentlyViewed` - Recently viewed products
- `Newsletter` - Newsletter subscribers

**Default database:** SQLite (set `DB_ENGINE=mysql` in `.env` for MySQL)

---

## 🧪 Run Tests

```bash
python manage.py test apps.store
python manage.py test --verbosity=2
```

---

## ⚙️ Configuration

### Razorpay Payment
Set in `.env`:
```env
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret
```

### Redis Cache (Optional)
Add to `.env`:
```env
CACHE_BACKEND=redis
REDIS_URL=redis://127.0.0.1:6379/1
```

Without Redis: Uses local memory cache automatically.

### Email
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True
```

In development (`DEBUG=True`), emails are printed to console.

### View Logs
```bash
# Windows
type logs\ecommerce.log

# Linux/Mac
tail -f logs/ecommerce.log
```

---

## 📊 Admin Panel

### Django Admin
Access: http://localhost:8000/admin/

Sections: Products, Orders, Customers, Reviews, Wishlists, Coupons, Newsletter, Recently Viewed

### Custom Admin Dashboard
Access: http://localhost:8000/admin-dashboard/

Features: Dashboard overview, product CRUD, order management (staff-only)

---

## 🌐 Multilingual Support

The project supports English and Hindi:
```python
# settings.py
LANGUAGES = [
    ('en', 'English'),
    ('hi', 'Hindi'),
]
```

Translation files are in the `locale/` directory.

---

## 💡 Usage Example

```javascript
// Add review with JavaScript
fetch('/api/add-review/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({
        product_id: 1,
        rating: 5,
        comment: 'Excellent!'
    })
});
```

---

## 🔧 Troubleshooting

**Migration errors:**
```bash
python manage.py migrate --fake store zero
python manage.py migrate store
```

**Redis not available:**
Leave `CACHE_BACKEND` unset in `.env` (uses local cache)

**Static files not loading:**
```bash
python manage.py collectstatic --no-input
```

---

**All features are production-ready!** 🚀
