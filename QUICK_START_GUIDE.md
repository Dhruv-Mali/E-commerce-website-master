# Quick Start Guide - E-Commerce Improvements

## 🚀 Immediate Steps to Apply Improvements

### Step 1: Create Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Update Your Templates

#### Add Enhanced JavaScript to Base Template
Replace or add alongside existing `cart.js`:

```html
<!-- In your base template -->
<script src="{% static 'js/cart_enhanced.js' %}"></script>
<link rel="stylesheet" href="{% static 'css/enhancements.css' %}">
```

#### Add Pagination to Store Template
In `store/templates/store/store.html`:

```html
<!-- After products loop -->
<nav aria-label="Page navigation">
    <ul class="pagination justify-content-center">
        {% if products.has_previous %}
            <li class="page-item">
                <a class="page-link" href="?page={{ products.previous_page_number }}{% if query %}&q={{ query }}{% endif %}{% if selected_category %}&category={{ selected_category }}{% endif %}">Previous</a>
            </li>
        {% endif %}
        
        <li class="page-item active">
            <span class="page-link">{{ products.number }} of {{ products.paginator.num_pages }}</span>
        </li>
        
        {% if products.has_next %}
            <li class="page-item">
                <a class="page-link" href="?page={{ products.next_page_number }}{% if query %}&q={{ query }}{% endif %}{% if selected_category %}&category={{ selected_category }}{% endif %}">Next</a>
            </li>
        {% endif %}
    </ul>
</nav>
```

#### Add Stock Badge to Product Cards
```html
<div class="product-card position-relative">
    {% if product.stock > 0 %}
        {% if product.stock < 10 %}
            <span class="stock-badge low-stock">Only {{ product.stock }} left</span>
        {% else %}
            <span class="stock-badge in-stock">In Stock</span>
        {% endif %}
    {% else %}
        <span class="stock-badge out-of-stock">Out of Stock</span>
    {% endif %}
    
    <!-- Rest of product card -->
</div>
```

#### Add Wishlist Button
```html
{% if user.is_authenticated %}
    <button class="btn btn-outline-danger wishlist-btn" onclick="toggleWishlist({{ product.id }}, this)">
        <i class="bi bi-heart"></i>
    </button>
{% endif %}
```

#### Add Related Products Section
In `store/templates/store/product_detail.html`:

```html
{% if related_products %}
<div class="related-products mt-5">
    <h3>Related Products</h3>
    <div class="row">
        {% for product in related_products %}
        <div class="col-md-3">
            <!-- Product card -->
        </div>
        {% endfor %}
    </div>
</div>
{% endif %}
```

### Step 3: Configure Stripe Webhooks

1. Go to Stripe Dashboard → Developers → Webhooks
2. Add endpoint: `https://yourdomain.com/extended/webhook/stripe/`
3. Select events: `checkout.session.completed`, `checkout.session.async_payment_failed`
4. Copy webhook secret to `.env`:
```env
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
```

### Step 4: Test Core Features

#### Test Stock Validation:
```python
# In Django shell
python manage.py shell

from store.models import Product
product = Product.objects.first()
product.stock = 5
product.save()

# Try adding 10 items to cart - should fail
```

#### Test Pagination:
```
Visit: http://127.0.0.1:8000/?page=2
```

#### Test Enhanced Cart:
- Add item to cart (should show toast notification)
- No page reload
- Loading spinner appears

### Step 5: Optional - Install Extended Features

```bash
# Install optional dependencies
pip install django-redis redis celery reportlab django-allauth

# Update settings.py - uncomment these lines:
# In INSTALLED_APPS:
'django_redis',
'allauth',
'allauth.account',

# In CACHES section - uncomment Redis configuration
```

### Step 6: Create Sample Data

```python
# Create coupons
from store.models_extended import Coupon
from django.utils import timezone
from datetime import timedelta

Coupon.objects.create(
    code='SAVE10',
    discount_percent=10,
    active=True,
    valid_from=timezone.now(),
    valid_to=timezone.now() + timedelta(days=30),
    usage_limit=100
)

# Create product variants
from store.models_extended import ProductVariant
from store.models import Product

product = Product.objects.first()
ProductVariant.objects.create(
    product=product,
    name='Size',
    value='Large',
    price_adjustment=50,
    stock=20
)
```

---

## 🎯 Feature-by-Feature Activation

### Enable Wishlist:
1. Run migrations
2. Add wishlist button to templates
3. Include `cart_enhanced.js`

### Enable Reviews:
1. Run migrations
2. Create review form in product detail template
3. Add review display section

### Enable Newsletter:
1. Run migrations
2. Add newsletter form to footer:
```html
<form id="newsletter-form">
    <input type="email" name="email" placeholder="Your email">
    <button type="submit">Subscribe</button>
</form>

<script>
document.getElementById('newsletter-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const email = this.email.value;
    
    fetch('/extended/newsletter/subscribe/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({email: email})
    })
    .then(response => response.json())
    .then(data => alert(data.message));
});
</script>
```

### Enable Order Status Tracking:
1. Update order history template:
```html
<span class="badge status-{{ order.status }}">
    {{ order.get_status_display }}
</span>
```

---

## 🔍 Verification Checklist

- [ ] Migrations applied successfully
- [ ] Pagination works on store page
- [ ] Cart updates without page reload
- [ ] Stock validation prevents overselling
- [ ] Toast notifications appear
- [ ] Related products show on detail page
- [ ] Product views increment
- [ ] Stripe webhook endpoint configured
- [ ] Security validators active
- [ ] Database indexes created

---

## 🐛 Troubleshooting

### Issue: Migrations fail
```bash
# Reset migrations (development only)
python manage.py migrate store zero
python manage.py makemigrations
python manage.py migrate
```

### Issue: JavaScript not working
- Check browser console for errors
- Verify `csrftoken` is defined
- Ensure jQuery/Bootstrap loaded

### Issue: Webhook not receiving events
- Check Stripe dashboard logs
- Verify endpoint URL is correct
- Ensure STRIPE_WEBHOOK_SECRET is set

### Issue: Import errors
```bash
# Install missing dependencies
pip install -r requirements_extended.txt
```

---

## 📊 Performance Monitoring

### Check Query Count:
```python
# In settings.py (development)
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### Monitor Page Load:
- Use browser DevTools Network tab
- Check for lazy-loaded images
- Verify pagination reduces load time

---

## 🎨 Customization Tips

### Change Pagination Size:
In `settings.py`:
```python
PAGINATION_PER_PAGE = 20  # Default is 12
```

### Customize Toast Duration:
In `cart_enhanced.js`:
```javascript
setTimeout(() => toast.remove(), 5000);  // 5 seconds
```

### Adjust Stock Warning Threshold:
In template:
```html
{% if product.stock < 20 %}  <!-- Change from 10 to 20 -->
    <span class="stock-badge low-stock">Low Stock</span>
{% endif %}
```

---

## 🚀 Production Deployment

### Before Going Live:
1. Set `DEBUG=False` in `.env`
2. Configure proper `SECRET_KEY`
3. Set up Redis for caching
4. Enable SSL/HTTPS settings
5. Configure email backend (not console)
6. Set up Stripe webhooks with production keys
7. Run `python manage.py collectstatic`
8. Set proper `ALLOWED_HOSTS`

### Security Checklist:
- [ ] DEBUG=False
- [ ] Strong SECRET_KEY
- [ ] HTTPS enabled
- [ ] CSRF_COOKIE_SECURE=True
- [ ] SESSION_COOKIE_SECURE=True
- [ ] Stripe keys in environment variables
- [ ] Database backups configured

---

## 📞 Need Help?

Check these files for detailed information:
- `IMPROVEMENTS_APPLIED.md` - Complete feature list
- `store/validators.py` - Security implementation
- `store/models_extended.py` - New models
- `store/views_extended.py` - New views
- `static/js/cart_enhanced.js` - Frontend enhancements

---

**You're all set! 🎉**

Start with Step 1 (migrations) and gradually enable features as needed.
