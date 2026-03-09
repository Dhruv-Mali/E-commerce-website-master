# 📁 PROJECT STRUCTURE & ARCHITECTURE

## Directory Layout

```
E-commerce-website-master-final/
│
├── 📂 apps/                          # Django applications
│   ├── 📂 loginsys/                  # Authentication & User Management
│   │   ├── migrations/               # Database migrations
│   │   ├── templates/                # Login/Register templates
│   │   ├── __init__.py
│   │   ├── apps.py                   # App configuration
│   │   ├── forms.py                  # User forms
│   │   ├── urls.py                   # URL routing
│   │   ├── views.py                  # Authentication views
│   │   └── views_secure.py           # Secure views (NEW)
│   │
│   └── 📂 store/                     # E-Commerce Core
│       ├── management/               # Custom management commands
│       ├── migrations/               # Database migrations
│       ├── templates/                # Product/Cart templates
│       ├── __init__.py
│       ├── admin.py                  # Django admin customization
│       ├── admin_extended.py         # Extended admin features
│       ├── api_views.py              # API endpoints
│       ├── apps.py                   # App configuration
│       ├── cache.py                  # Caching utilities
│       ├── context_processors.py     # Template context
│       ├── forms.py                  # Product forms
│       ├── logging_utils.py          # Logging utilities
│       ├── models.py                 # Database models
│       ├── models_extended.py        # Extended models
│       ├── security_middleware.py    # Security middleware (NEW)
│       ├── tests.py                  # Unit tests
│       ├── urls.py                   # URL routing
│       ├── utils.py                  # Utility functions
│       ├── validators.py             # Input validators
│       ├── views.py                  # Main views
│       └── views_secure.py           # Secure views (NEW)
│
├── 📂 config/                        # Django Configuration
│   ├── 📂 ecommerce/
│   │   ├── __init__.py
│   │   ├── settings.py               # Main settings
│   │   ├── settings_secure.py        # Secure settings (NEW)
│   │   ├── urls.py                   # URL configuration
│   │   └── wsgi.py                   # WSGI application
│   └── __init__.py
│
├── 📂 core/                          # Base Templates & Static Files
│   ├── 📂 static/
│   │   ├── admin/                    # Admin static files
│   │   ├── css/                      # Stylesheets
│   │   │   ├── landing.css
│   │   │   ├── main.css
│   │   │   └── tech_theme.css
│   │   ├── images/                   # Images & Icons
│   │   └── js/                       # JavaScript
│   │       └── cart.js
│   ├── 📂 templates/
│   │   ├── footer.html
│   │   ├── index.html
│   │   ├── landing_base.html
│   │   └── navbar.html
│   └── __init__.py
│
├── 📂 database/                      # Database Management
│   ├── backup_db.py                  # Backup script
│   ├── restore_db.py                 # Restore script
│   └── README.md                     # Database docs
│
├── 📂 logs/                          # Application Logs
│   └── ecommerce.log                 # Main log file
│
├── 📂 media/                         # User Uploads
│   └── products/                     # Product images
│
├── 📂 staticfiles/                   # Collected static files
│   ├── admin/
│   ├── css/
│   ├── images/
│   └── js/
│
├── 📂 utils/                         # Utility Scripts
│   ├── scripts/
│   │   ├── populate_database.py
│   │   └── setup_db.py
│   └── __init__.py
│
├── 📂 locale/                        # Internationalization
│
├── 📄 .env                           # Environment variables (NEVER COMMIT)
├── 📄 .env.example                   # Environment template (NEW)
├── 📄 .gitignore                     # Git ignore rules
├── 📄 db.sqlite3                     # SQLite database
├── 📄 docker-compose.yml             # Docker configuration
├── 📄 Dockerfile                     # Docker image
├── 📄 manage.py                      # Django CLI
├── 📄 nginx.conf                     # Nginx configuration
├── 📄 requirements.txt               # Python dependencies
├── 📄 requirements-docker.txt        # Docker dependencies
├── 📄 README.md                      # Project documentation
├── 📄 SETUP.md                       # Setup guide
├── 📄 SECURITY_HARDENING.md          # Security guide (NEW)
└── 📄 walkthrough.md.resolved        # Walkthrough guide
```

---

## Key Components

### 1. Authentication System (loginsys)
**Purpose:** User registration, login, and profile management

**Files:**
- `views.py` - Login/Register/Profile views
- `forms.py` - User forms with validation
- `urls.py` - Authentication routes
- `templates/` - Login/Register templates

**Features:**
- User registration with validation
- Secure password authentication
- Profile management
- Rate limiting on login attempts

### 2. E-Commerce Core (store)
**Purpose:** Product catalog, shopping cart, orders, and payments

**Files:**
- `models.py` - Database models (Product, Order, Customer)
- `views.py` - Product/Cart/Checkout views
- `api_views.py` - API endpoints (Reviews, Wishlist)
- `utils.py` - Payment processing (Razorpay)
- `admin.py` - Django admin customization

**Features:**
- Product catalog with search/filter
- Shopping cart (guest & authenticated)
- Order management
- Payment processing (Razorpay)
- Reviews & ratings
- Wishlist
- Newsletter

### 3. Configuration (config)
**Purpose:** Django settings and URL routing

**Files:**
- `settings.py` - Main Django settings
- `urls.py` - URL routing
- `wsgi.py` - WSGI application

**Key Settings:**
- Database configuration
- Email settings
- Security settings
- Static files
- Logging

### 4. Static Files (core/static)
**Purpose:** CSS, JavaScript, and images

**Files:**
- `css/` - Stylesheets
- `js/` - JavaScript files
- `images/` - Icons and images

### 5. Templates (core/templates & app templates)
**Purpose:** HTML templates for rendering

**Structure:**
- Base templates in `core/templates/`
- App-specific templates in `app/templates/`
- Template inheritance for consistency

---

## Database Models

### Customer
```python
- user (OneToOne User)
- name (CharField)
- email (CharField)
```

### Product
```python
- name (CharField)
- price (IntegerField)
- description (TextField)
- image (ImageField)
- stock (IntegerField)
- category (CharField)
- digital (BooleanField)
- views (IntegerField)
- created_at (DateTimeField)
- updated_at (DateTimeField)
```

### Order
```python
- customer (ForeignKey Customer)
- date_ordered (DateTimeField)
- complete (BooleanField)
- transaction_id (CharField)
- razorpay_payment_id (CharField)
- status (CharField)
```

### OrderItem
```python
- product (ForeignKey Product)
- order (ForeignKey Order)
- quantity (IntegerField)
- date_added (DateTimeField)
```

### ShippingAddress
```python
- customer (ForeignKey Customer)
- order (ForeignKey Order)
- address (CharField)
- city (CharField)
- state (CharField)
- zipcode (CharField)
- date_added (DateTimeField)
```

---

## URL Routing

### Authentication URLs (`/l/`)
- `GET /l/` - Login page
- `POST /l/` - Login submission
- `GET /l/register/` - Register page
- `POST /l/register/` - Register submission
- `GET /l/logout/` - Logout
- `GET /l/profile/` - User profile
- `POST /l/profile/` - Update profile

### Store URLs (`/store/`)
- `GET /store/` - Product listing
- `GET /store/product/<id>/` - Product detail
- `GET /store/cart/` - Shopping cart
- `GET /store/checkout/` - Checkout page
- `POST /store/checkout/` - Process checkout
- `GET /store/order-history/` - Order history
- `GET /store/wishlist/` - Wishlist

### API URLs (`/api/`)
- `POST /api/add-review/` - Add product review
- `POST /api/toggle-wishlist/` - Add/remove wishlist
- `GET /api/wishlist/` - Get wishlist
- `POST /api/subscribe-newsletter/` - Subscribe

### Admin URLs (`/admin/`)
- Django admin interface
- Custom admin views

---

## Security Architecture

### Middleware Stack
1. SecurityMiddleware - HTTPS redirect
2. SecurityHeadersMiddleware - Security headers
3. RateLimitMiddleware - Rate limiting
4. SQLInjectionProtectionMiddleware - SQL injection detection
5. XSSProtectionMiddleware - XSS detection
6. SessionMiddleware - Session management
7. AuthenticationMiddleware - User authentication
8. CsrfViewMiddleware - CSRF protection

### Input Validation
- All user inputs sanitized
- Email validation
- Phone validation
- SQL injection detection
- XSS detection

### Authentication
- Django's built-in auth system
- Password hashing (PBKDF2)
- Session-based authentication
- Rate limiting on login

### Authorization
- @login_required decorator
- @staff_member_required decorator
- Permission checks in views

---

## Data Flow

### User Registration
1. User fills registration form
2. Form validation (email, password strength)
3. User created in database
4. User logged in automatically
5. Redirect to store

### Product Purchase
1. User adds product to cart
2. Cart stored in database (authenticated) or cookies (guest)
3. User proceeds to checkout
4. Shipping address collected
5. Razorpay payment gateway initialized
6. Payment processed
7. Order marked as complete
8. Confirmation email sent
9. Stock reduced

### Order Processing
1. Order created with status "pending"
2. Payment verified
3. Order status changed to "processing"
4. Admin notified
5. Order shipped
6. Customer notified
7. Order status changed to "delivered"

---

## Performance Optimization

### Caching
- Product list caching
- Category caching
- User session caching

### Database
- Indexed fields (category, created_at, views)
- Select_related for foreign keys
- Prefetch_related for reverse relations

### Static Files
- WhiteNoise for static file serving
- CSS/JS minification
- Image optimization

### Pagination
- 12 products per page
- Reduces database queries
- Improves page load time

---

## Deployment Architecture

### Development
- SQLite database
- Django development server
- Console email backend

### Production
- MySQL database
- Gunicorn WSGI server
- Nginx reverse proxy
- HTTPS/SSL
- Redis caching (optional)

### Docker
- Docker Compose for orchestration
- Django container
- MySQL container
- Nginx container

---

## File Naming Conventions

- `models.py` - Database models
- `views.py` - View functions
- `urls.py` - URL routing
- `forms.py` - Django forms
- `admin.py` - Admin customization
- `utils.py` - Utility functions
- `validators.py` - Input validators
- `tests.py` - Unit tests
- `templates/` - HTML templates
- `static/` - CSS, JS, images
- `migrations/` - Database migrations

---

## Best Practices

### Code Organization
- One model per file (or related models)
- One view per URL pattern
- Separate business logic from views
- Use utility functions for common tasks

### Database
- Use migrations for schema changes
- Index frequently queried fields
- Use select_related/prefetch_related
- Avoid N+1 queries

### Security
- Validate all inputs
- Escape all outputs
- Use CSRF protection
- Implement rate limiting
- Log security events

### Performance
- Cache frequently accessed data
- Optimize database queries
- Minimize HTTP requests
- Compress static files

### Testing
- Write unit tests
- Test edge cases
- Test security features
- Test payment processing

---

## Maintenance

### Regular Tasks
- Monitor error logs
- Review security logs
- Update dependencies
- Backup database
- Test backups

### Monitoring
- Error rates
- Response times
- Database performance
- Server resources
- Payment failures

### Updates
- Django security updates
- Dependency updates
- Security patches
- Feature updates
