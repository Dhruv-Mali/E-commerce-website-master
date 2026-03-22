# 📁 PROJECT STRUCTURE & ARCHITECTURE

## Directory Layout

```
E-commerce-website-master-final/
│
├── 📂 apps/                          # Django applications
│   ├── __init__.py
│   │
│   ├── 📂 loginsys/                  # Authentication & User Management
│   │   ├── migrations/               # Database migrations
│   │   ├── templates/loginsys/       # Auth templates
│   │   │   ├── login.html            # Login page
│   │   │   ├── registerUser.html     # Registration page
│   │   │   └── profile.html          # User profile
│   │   ├── __init__.py
│   │   ├── apps.py                   # App configuration
│   │   ├── forms.py                  # User forms
│   │   ├── urls.py                   # URL routing
│   │   ├── views.py                  # Authentication views
│   │   └── views_secure.py           # Secure views reference
│   │
│   └── 📂 store/                     # E-Commerce Core
│       ├── management/               # Custom management commands
│       ├── migrations/               # Database migrations
│       ├── templates/
│       │   ├── store/                # Store templates
│       │   │   ├── landing.html      # Landing page
│       │   │   ├── store.html        # Product catalog
│       │   │   ├── product_detail.html  # Product detail
│       │   │   ├── cart.html         # Shopping cart
│       │   │   ├── checkout.html     # Checkout page
│       │   │   ├── order_success.html   # Order confirmation
│       │   │   ├── order_history.html   # Order history
│       │   │   ├── wishlist.html     # Wishlist page
│       │   │   ├── invoice_pdf.html  # PDF invoice template
│       │   │   ├── cancelled.html    # Payment cancelled
│       │   │   └── payment_failed.html  # Payment failed
│       │   └── admin/                # Custom admin templates
│       │       ├── dashboard.html    # Admin dashboard
│       │       ├── products.html     # Product management
│       │       ├── add_product.html  # Add product
│       │       ├── edit_product.html # Edit product
│       │       ├── delete_product.html  # Delete product
│       │       └── orders.html       # Order management
│       ├── __init__.py
│       ├── admin.py                  # Django admin customization
│       ├── admin_extended.py         # Extended admin (Reviews, Wishlist, Coupons)
│       ├── api_views.py              # API endpoints
│       ├── apps.py                   # App configuration
│       ├── cache.py                  # Caching utilities
│       ├── context_processors.py     # Template context (cart data)
│       ├── forms.py                  # Product forms
│       ├── logging_utils.py          # Logging helpers
│       ├── models.py                 # Core models (Customer, Product, Order, etc.)
│       ├── models_extended.py        # Extended models (Review, Wishlist, Coupon, etc.)
│       ├── security_middleware.py    # Security middleware
│       ├── test_razorpay.py          # Razorpay integration tests
│       ├── tests.py                  # Unit tests
│       ├── urls.py                   # URL routing
│       ├── utils.py                  # Utility functions (Razorpay payment)
│       ├── validators.py             # Input validators
│       ├── views.py                  # Main views
│       └── views_secure.py           # Secure views reference
│
├── 📂 config/                        # Django Configuration
│   ├── __init__.py
│   └── 📂 ecommerce/
│       ├── __init__.py
│       ├── settings.py               # Main settings
│       ├── settings_secure.py        # Secure settings reference
│       ├── urls.py                   # Root URL configuration
│       └── wsgi.py                   # WSGI application
│
├── 📂 core/                          # Base Templates & Static Files
│   ├── __init__.py
│   ├── 📂 static/
│   │   ├── css/
│   │   │   ├── landing.css           # Landing page styles
│   │   │   ├── main.css              # Main stylesheet
│   │   │   └── tech_theme.css        # Tech theme styles
│   │   ├── images/                   # Images & Icons
│   │   └── js/
│   │       └── cart.js               # Cart JavaScript
│   └── 📂 templates/
│       ├── footer.html               # Site footer
│       ├── index.html                # Base index template
│       ├── landing_base.html         # Landing page base
│       └── navbar.html               # Navigation bar
│
├── 📂 database/                      # Database Management
│   ├── backup_db.py                  # Backup script
│   ├── restore_db.py                 # Restore script
│   └── README.md                     # Database docs
│
├── 📂 locale/                        # Internationalization (i18n)
│   └── (translation files for EN, HI)
│
├── 📂 logs/                          # Application Logs
│   └── ecommerce.log                 # Main log file
│
├── 📂 media/                         # User Uploads
│   └── products/                     # Product images
│
├── 📂 staticfiles/                   # Collected static files (WhiteNoise)
│
├── 📂 utils/                         # Utility Scripts
│   ├── __init__.py
│   └── scripts/
│       ├── populate_database.py
│       └── setup_db.py
│
├── 📄 .env                           # Environment variables (NEVER COMMIT)
├── 📄 .dockerignore                  # Docker ignore rules
├── 📄 .gitignore                     # Git ignore rules
├── 📄 db.sqlite3                     # SQLite database (development)
├── 📄 docker-compose.yml             # Docker Compose (web + mysql + redis)
├── 📄 Dockerfile                     # Docker image (Python 3.12)
├── 📄 manage.py                      # Django CLI
├── 📄 nginx.conf                     # Nginx configuration
├── 📄 requirements.txt               # Python dependencies
├── 📄 requirements-docker.txt        # Docker-specific dependencies
├── 📄 reset_admin.py                 # Admin reset utility
├── 📄 test_razorpay.py               # Razorpay test script
└── 📄 README.md                      # Project documentation
```

---

## Key Components

### 1. Authentication System (loginsys)
**Purpose:** User registration, login, and profile management

**Files:**
- `views.py` - Login/Register/Profile views
- `forms.py` - User forms with validation
- `urls.py` - Authentication routes (`/l/` and `/auth/`)
- `templates/loginsys/` - Login, Register, Profile templates

**Features:**
- User registration with form validation
- Secure password authentication
- Profile management
- Rate limiting on login attempts (via security middleware)

### 2. E-Commerce Core (store)
**Purpose:** Product catalog, shopping cart, orders, payments, and admin

**Files:**
- `models.py` - Core models (Customer, Product, Order, OrderItem, ShippingAddress)
- `models_extended.py` - Extended models (ProductReview, Wishlist, Coupon, RecentlyViewed, Newsletter)
- `views.py` - Product/Cart/Checkout/Admin views + PDF invoice generation
- `api_views.py` - API endpoints (Reviews, Wishlist, Newsletter)
- `utils.py` - Razorpay payment processing
- `admin.py` - Django admin customization
- `admin_extended.py` - Admin for extended models
- `security_middleware.py` - Security headers, rate limiting, SQL injection & XSS protection
- `cache.py` - Caching utilities
- `validators.py` - Input validation helpers
- `context_processors.py` - Cart context for all templates

**Features:**
- Product catalog with search/filter/pagination
- Shopping cart (guest via cookies & authenticated via database)
- Razorpay payment integration with signature verification
- Order management with status tracking
- PDF invoice generation
- Reviews & ratings (1-5 stars, verified purchase badges)
- Wishlist
- Coupon/discount system
- Newsletter subscription
- Recently viewed products
- Custom admin dashboard (staff-only)

### 3. Configuration (config/ecommerce)
**Purpose:** Django settings and URL routing

**Files:**
- `settings.py` - Main Django settings (DB, email, cache, security, logging)
- `urls.py` - Root URL routing
- `wsgi.py` - WSGI application

**Key Configuration:**
- Dual database support (SQLite / MySQL)
- WhiteNoise static file serving
- Email backend (console in dev, SMTP in prod)
- Razorpay payment keys
- Security settings (enabled when DEBUG=False)
- Logging with rotating file handler
- i18n support (English, Hindi)

### 4. Static Files (core/static)
**Purpose:** CSS, JavaScript, and images

**CSS Files:**
- `landing.css` - Landing page styles
- `main.css` - Main application styles
- `tech_theme.css` - Tech theme styles

**JavaScript:**
- `cart.js` - Cart add/remove/update functionality

### 5. Templates (core/templates & app templates)
**Purpose:** HTML templates for rendering

**Structure:**
- Base templates in `core/templates/` (navbar, footer, landing base, index)
- Store templates in `apps/store/templates/store/` (11 pages)
- Admin templates in `apps/store/templates/admin/` (6 pages)
- Auth templates in `apps/loginsys/templates/loginsys/` (3 pages)
- Template inheritance for consistency

---

## Database Models

### Core Models (models.py)

#### Customer
```python
- user (OneToOne → User)
- name (CharField)
- email (CharField, indexed)
```

#### Product
```python
- name (CharField, indexed)
- price (IntegerField)
- description (TextField)
- image (ImageField → products/)
- stock (IntegerField, default=100)
- category (CharField, indexed)
- digital (BooleanField)
- views (IntegerField)
- created_at (DateTimeField, auto)
- updated_at (DateTimeField, auto)
```

#### Order
```python
- customer (ForeignKey → Customer)
- date_ordered (DateTimeField, auto)
- complete (BooleanField)
- transaction_id (CharField, unique, indexed)
- razorpay_payment_id (CharField)
- status (CharField: pending/processing/shipped/delivered/cancelled)
```

#### OrderItem
```python
- product (ForeignKey → Product)
- order (ForeignKey → Order)
- quantity (IntegerField)
- date_added (DateTimeField, auto)
```

#### ShippingAddress
```python
- customer (ForeignKey → Customer)
- order (ForeignKey → Order)
- address (CharField)
- city (CharField)
- state (CharField)
- zipcode (CharField)
- date_added (DateTimeField, auto)
```

### Extended Models (models_extended.py)

#### ProductReview
```python
- product (ForeignKey → Product)
- user (ForeignKey → User)
- rating (IntegerField, 1-5)
- comment (TextField)
- verified_purchase (BooleanField)
- created_at / updated_at
```

#### Wishlist
```python
- user (ForeignKey → User)
- product (ForeignKey → Product)
- added_at (DateTimeField)
```

#### Coupon
```python
- code (CharField, unique)
- discount_percent (IntegerField, 1-100)
- valid_from / valid_to (DateTimeField)
- active (BooleanField)
- max_uses / used_count (IntegerField)
```

#### RecentlyViewed
```python
- user (ForeignKey → User)
- product (ForeignKey → Product)
- viewed_at (DateTimeField)
```

#### Newsletter
```python
- email (EmailField, unique)
- subscribed_at (DateTimeField)
- active (BooleanField)
```

---

## URL Routing

### Root URLs (config/ecommerce/urls.py)
- `/admin/` → Django admin
- `/` → Store app (includes landing & all store routes)
- `/l/` → Login system
- `/auth/` → Login system (legacy path)
- `/i18n/` → Language switching

### Store URLs
- `GET /` → Landing page
- `GET /store/` → Product catalog
- `GET /product/<id>/` → Product detail
- `GET /cart/` → Shopping cart
- `GET /checkout/` → Checkout page
- `POST /process-order/` → Process order + Razorpay payment
- `GET /payment-success/` → Payment success page
- `GET /payment-cancelled/` → Payment cancelled page
- `GET /orders/` → Order history
- `GET /wishlist/` → Wishlist page
- `POST /update-item/` → Update cart item (AJAX)
- `GET /invoice/<order_id>/` → Download PDF invoice

### Custom Admin URLs
- `GET /admin-dashboard/` → Admin dashboard
- `GET /admin-products/` → Product list
- `GET /admin-add-product/` → Add product form
- `GET /admin-edit-product/<id>/` → Edit product form
- `POST /admin-delete-product/<id>/` → Delete product
- `GET /admin-orders/` → Order management

### API URLs
- `POST /api/add-review/` → Add product review
- `POST /api/toggle-wishlist/` → Toggle wishlist item
- `GET /api/wishlist/` → Get wishlist
- `POST /api/subscribe-newsletter/` → Newsletter subscribe

### Authentication URLs (`/l/`)
- `GET /l/` → Login page
- `POST /l/` → Login submission
- `GET /l/register/` → Register page
- `POST /l/register/` → Register submission
- `GET /l/logout/` → Logout
- `GET /l/profile/` → User profile
- `POST /l/profile/` → Update profile

---

## Security Architecture

### Middleware Stack (settings.py)
1. `SecurityMiddleware` - Django security (HTTPS redirect, etc.)
2. `WhiteNoiseMiddleware` - Static file serving
3. `SessionMiddleware` - Session management
4. `LocaleMiddleware` - Language detection (i18n)
5. `CommonMiddleware` - URL normalization
6. `CsrfViewMiddleware` - CSRF protection
7. `AuthenticationMiddleware` - User authentication
8. `MessageMiddleware` - Flash messages
9. `XFrameOptionsMiddleware` - Clickjacking protection

### Custom Security Middleware (security_middleware.py)
- `SecurityHeadersMiddleware` - Security response headers
- `RateLimitMiddleware` - Request rate limiting
- `SQLInjectionProtectionMiddleware` - SQL injection detection
- `XSSProtectionMiddleware` - XSS detection

### Production Security (DEBUG=False)
- `SECURE_SSL_REDIRECT = True`
- `SESSION_COOKIE_SECURE = True`
- `CSRF_COOKIE_SECURE = True`
- `SECURE_BROWSER_XSS_FILTER = True`
- `X_FRAME_OPTIONS = 'DENY'`

---

## Data Flow

### Product Purchase
1. User browses products on landing/store page
2. User adds product to cart (AJAX via `update-item/`)
3. Cart stored in database (authenticated) or cookies (guest)
4. User proceeds to checkout
5. Shipping address collected
6. Razorpay payment gateway initialized
7. Payment processed & verified (signature check)
8. Order marked as complete, stock reduced
9. Confirmation page shown with invoice download link

### PDF Invoice Generation
1. User visits order history or order success page
2. Clicks "Download Invoice" link
3. Server generates PDF from `invoice_pdf.html` template
4. PDF returned as downloadable file

---

## Deployment Architecture

### Development
- SQLite database
- Django development server (`runserver`)
- Console email backend
- Local memory cache

### Production
- MySQL database
- Gunicorn WSGI server
- Nginx reverse proxy
- HTTPS/SSL via Let's Encrypt
- Redis caching (optional)
- WhiteNoise static files

### Docker (docker-compose.yml)
- `web` - Django app (Python 3.12-slim)
- `mysql` - MySQL 8.0
- `redis` - Redis 7 Alpine

---

## Best Practices

### Code Organization
- Separate core and extended models
- API views in dedicated `api_views.py`
- Security middleware in dedicated module
- Context processors for cross-template data
- Utility functions for payment processing

### Database
- Use migrations for schema changes
- Indexed fields (category, created_at, views, email, transaction_id)
- Use `select_related` / `prefetch_related` for query optimization
- Unique constraints on orders (one incomplete order per customer)

### Security
- Validate all inputs (`validators.py`)
- Escape all outputs (Django template auto-escaping)
- CSRF on all POST forms
- Staff-only access for admin views
- Razorpay signature verification on payments
