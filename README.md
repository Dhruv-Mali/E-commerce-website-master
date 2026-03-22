# 🛒 E-Commerce Website with OTP Authentication

A full-featured, **production-ready** e-commerce platform built with Django, MySQL/SQLite, and modern web technologies featuring OTP authentication, Razorpay payment integration, PDF invoices, multilingual support, comprehensive admin interface, and **enterprise-grade security**.

**Status:** ✅ SECURE | ✅ TESTED | ✅ DOCUMENTED | ✅ PRODUCTION-READY

## ✨ Key Features

### 🔐 Authentication System
- 🔑 **Password Login** - Username/password authentication with strong validation
- 👤 **User Registration** - Secure registration with form validation
- 📞 **OTP Support** - SMS-Based OTP via Twilio integration (optional)
- 🛡️ **Rate Limiting** - Brute force protection
- 🔒 **Session Security** - HttpOnly, Secure, SameSite cookies

### 🏪 Core E-Commerce Features
- 🛍️ **Product Catalog** - Categories, filtering, search with XSS protection
- 🛒 **Smart Shopping Cart** - Guest (cookie-based) & authenticated (database) users with stock validation
- 💳 **Razorpay Payment** - Secure payment processing with signature verification
- 📦 **Order Management** - Complete order tracking with status updates (pending → processing → shipped → delivered)
- 🧾 **PDF Invoices** - Downloadable invoice generation for orders
- 👤 **User Profiles** - Account management & order history
- 📧 **Email Notifications** - Order confirmations & updates
- 🔐 **CSRF Protection** - All forms protected

### ⭐ Advanced Features
- ⭐ **Reviews & Ratings** - 1-5 star system with verified purchase badges
- ❤️ **Wishlist** - Save favorite products
- 📧 **Newsletter** - Email subscription management
- 🎟️ **Coupons** - Discount codes with validation
- 👁️ **Recently Viewed** - Product history tracking
- 📊 **Custom Admin Dashboard** - Product, order & customer management with permission checks
- 🔍 **Full-Text Search** - Advanced filtering with SQL injection prevention
- 🌐 **Multilingual (i18n)** - English & Hindi language support
- 🏠 **Landing Page** - Modern landing page with tech theme

### 🔒 Security Features
- ✅ **30+ Vulnerabilities Fixed** - Enterprise-grade security
- 🛡️ **Security Headers** - X-Frame-Options, CSP, HSTS
- 🔐 **Input Validation** - All user inputs sanitized
- 🚫 **SQL Injection Prevention** - Parameterized queries + detection
- 🚫 **XSS Prevention** - Input escaping + CSP headers
- ⏱️ **Rate Limiting** - Brute force protection
- 📝 **Comprehensive Logging** - Security event tracking
- 🔒 **Secure Sessions** - HttpOnly, Secure, SameSite cookies

---

## 📚 Documentation

### Available Guides
- **[SECURITY_HARDENING.md](SECURITY_HARDENING.md)** - Security best practices & fixes
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Project architecture & organization
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Production deployment guide
- **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** - Find any information
- **[SETUP.md](SETUP.md)** - Feature setup & API reference
- **[COMPLETION_SUMMARY.md](COMPLETION_SUMMARY.md)** - Project audit summary
- **[IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md)** - Implementation status

---

## 🚀 Quick Start Guide

### Prerequisites
```
- Python 3.10+ (Docker uses 3.12)
- MySQL 8.0+ (optional, SQLite by default)
- Razorpay Account (for payments)
- Twilio Account (optional, for OTP)
```

### Step 1: Clone & Setup
```bash
git clone <repository-url>
cd E-commerce-website-master-final
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment
Create a `.env` file in the project root:
```env
# Django
DEBUG=True
SECRET_KEY=your-generated-50-char-key

# Database (SQLite used by default, set to mysql for MySQL)
DB_ENGINE=sqlite3
DB_NAME=ecommerce_db
DB_USER=root
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=3306

# Payment - Razorpay
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Generate Strong SECRET_KEY:**
```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
# Copy output to .env
```

### Step 4: Initialize Database
```bash
python manage.py migrate
python manage.py createsuperuser

# Verify security settings
python manage.py check --deploy
```

### Step 5: Start Server
```bash
python manage.py runserver
```

### Step 6: Access Application
```
Website:  http://127.0.0.1:8000/         (Landing Page)
Store:    http://127.0.0.1:8000/store/    (Product Catalog)
Admin:    http://127.0.0.1:8000/admin/    (Django Admin)
Login:    http://127.0.0.1:8000/l/        (User Login)
```

---

## 🔒 Security & Best Practices

### Security Features Implemented
✅ **CSRF Protection** - All POST requests protected
✅ **SQL Injection Prevention** - Parameterized queries + detection middleware
✅ **XSS Prevention** - Input escaping + Content Security Policy
✅ **Rate Limiting** - Brute force protection
✅ **Session Security** - HttpOnly, Secure, SameSite cookies
✅ **Security Headers** - X-Frame-Options, CSP, HSTS, etc.
✅ **Input Validation** - All user inputs sanitized
✅ **Error Handling** - Generic messages to users, detailed logs for admins
✅ **Logging** - Comprehensive security event tracking
✅ **Payment Verification** - Razorpay signature verification

### Production Checklist
- [ ] DEBUG = False
- [ ] SECRET_KEY = strong random (50+ chars)
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS/SSL enabled
- [ ] Database password changed
- [ ] Email credentials secured
- [ ] Razorpay keys in production mode
- [ ] Backups configured
- [ ] Monitoring setup

**See [SECURITY_HARDENING.md](SECURITY_HARDENING.md) for complete security guide**

---

## 🔍 Troubleshooting

### Payment Not Working
```
Check:
1. Razorpay keys in .env
2. Razorpay account in test mode
3. Check Razorpay dashboard for errors
4. Verify webhook configuration
```

### Static Files Not Loading
```bash
python manage.py collectstatic --no-input
dir staticfiles\
```

### Database Connection Error
```bash
# For SQLite (default) - check db.sqlite3 exists
# For MySQL:
mysql -u root -p -e "SELECT 1"
```

**See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md#troubleshooting) for more troubleshooting**

---

## 📊 Admin Dashboard

### Django Admin
**Access:** http://localhost:8000/admin/

**Sections:**
- Users & Profiles
- Products & Inventory
- Product Images
- Reviews & Ratings
- Orders & Order Items
- Wishlists
- Coupons & Codes
- Newsletter Subscribers
- Recently Viewed

### Custom Admin Panel
**Access:** http://localhost:8000/admin-dashboard/

**Features:**
- Dashboard overview
- Product management (add/edit/delete)
- Order management
- Staff-only access with permission checks

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | Django 4.2.2 | Web framework |
| **Database** | SQLite / MySQL 8.0+ | Data storage |
| **Frontend** | HTML5, CSS3, Bootstrap | UI/UX |
| **JavaScript** | Vanilla JS + jQuery | Interactivity |
| **Payments** | Razorpay API | Transaction processing |
| **SMS/OTP** | Twilio API | Phone authentication (optional) |
| **Static Files** | WhiteNoise | Static file serving |
| **Server** | Gunicorn + Nginx | Production deployment |
| **Cache** | Redis / Local Memory | Performance boost |
| **Container** | Docker Compose | Orchestration |
| **i18n** | Django i18n | English & Hindi |

---

## 📦 Dependencies

### Core Requirements
```
Django==4.2.2
djangorestframework==3.14.0
PyMySQL==1.1.2
Pillow==12.1.1
razorpay==1.4.2
twilio==9.10.1
python-dotenv==1.2.1
python-decouple==3.8
whitenoise==6.11.0
requests==2.32.5
```

**View all:** `requirements.txt`

---

## 🐳 Docker Deployment

### Quick Start with Docker Compose

**1. Build and Start:**
```bash
docker-compose build
docker-compose up -d
```

**2. Initialize:**
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

**3. Access:**
- Website: http://localhost:8000/
- Admin: http://localhost:8000/admin/
- Database (MySQL): localhost:3307

**4. Useful Commands:**
```bash
# View logs
docker-compose logs -f web

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Stop services
docker-compose down

# Remove all data
docker-compose down -v
```

**Services:**
- `web` - Django app (Python 3.12)
- `mysql` - MySQL 8.0 database
- `redis` - Redis 7 cache

---

## 🔧 Management Commands

```bash
# Database Operations
python manage.py migrate                    # Apply migrations
python manage.py makemigrations             # Create migrations
python manage.py createsuperuser            # Create admin user
python manage.py collectstatic              # Collect static files

# Security
python manage.py check --deploy             # Check production settings

# Testing
python manage.py test                       # Run all tests
python manage.py test apps.store            # Test specific app
python manage.py test --verbosity=2         # Verbose output

# Database Backup
python database/backup_db.py               # Backup database
python database/restore_db.py <file>       # Restore database

# Utilities
python manage.py shell                      # Django Python shell
python manage.py runserver                  # Start dev server
python manage.py dumpdata > backup.json    # Export data
python manage.py loaddata backup.json      # Import data
```

---

## 📚 Feature Documentation

### 💳 Smart Shopping Cart

**For Guest Users (Cookie-Based):**
- Stored in browser cookies (JSON format)
- Persists across sessions
- Automatic cleanup on cart clearing

**For Authenticated Users (Database):**
- Stored in database
- Persistent across devices
- Real-time syncing
- Complete history preserved

### ⭐ Reviews & Ratings

**Features:**
- 1-5 star rating system
- Text comments
- Average rating display
- Review count display
- Verified purchase badges
- One review per user per product

### ❤️ Wishlist System

**Functionality:**
- One-click add/remove toggle
- Persistent database storage
- Quick cart addition
- User-specific wishlists

### 🎟️ Coupon System

**Admin Features:**
- Create discount codes
- Set validity period
- Usage limits
- Percentage-based discounts
- Auto-validation

**Customer Features:**
- Apply at checkout
- View discount before purchase
- Error messages for invalid codes

### 📧 Newsletter

**Subscription:**
- Footer subscribe form
- Email validation
- Automatic list management

### 🧾 PDF Invoices

**Features:**
- Downloadable PDF invoices for completed orders
- Available from order history and order success pages
- Includes order details, items, pricing, and shipping info

### 🌐 Multilingual Support

**Languages:**
- English (default)
- Hindi

**Usage:**
- Language switcher in the UI
- Translation files in `locale/` directory

---

## 🚀 Deployment

### Local Development
```bash
python manage.py runserver
# http://localhost:8000
```

### Docker (Recommended)
```bash
docker-compose up -d
# http://localhost:8000
```

### Production (Manual)
```bash
# Collect static files
python manage.py collectstatic --no-input

# Run with Gunicorn
gunicorn config.ecommerce.wsgi --bind 0.0.0.0:8000

# Use Nginx as reverse proxy (see nginx.conf)
```

---

## 💡 Best Practices

### Development Tips
- ✅ Keep DEBUG=True locally
- ✅ Use .env for secrets
- ✅ Review logs regularly (`logs/ecommerce.log`)
- ✅ Use virtual environment

### Production Tips
- ✅ Set DEBUG=False
- ✅ Use strong SECRET_KEY
- ✅ Enable HTTPS/SSL
- ✅ Regular database backups
- ✅ Monitor error logs
- ✅ Set up alerts
- ✅ Regular dependency updates

### Performance
- ✅ Use Redis caching
- ✅ Optimize queries
- ✅ Enable compression (WhiteNoise)
- ✅ Use CDN
- ✅ Lazy load images

---

## 🧪 Testing

**Run Tests:**
```bash
# All tests
python manage.py test

# Specific app
python manage.py test apps.store

# With details
python manage.py test --verbosity=2
```

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/Name`
3. Make changes
4. Commit: `git commit -m 'Add feature'`
5. Push: `git push origin feature/Name`
6. Create Pull Request

---

## 📄 License

Educational use. Modify and use freely.

---

## 📞  Support
Dhruv Mali: Dhruvmali9039@gmail.com

**Having Issues?**
1. Check documentation
2. Review `logs/ecommerce.log`
3. See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md#troubleshooting)
4. Create GitHub issue with logs

---

## ✅ Project Status

| Component | Status |
|-----------|--------|
| Core Features | ✅ Complete |
| Authentication | ✅ Complete |
| Razorpay Payments | ✅ Complete |
| PDF Invoices | ✅ Complete |
| Custom Admin Panel | ✅ Complete |
| Docker Support | ✅ Complete |
| i18n (EN/HI) | ✅ Complete |
| Security Hardening | ✅ Complete |
| Documentation | ✅ Complete |

---

## 📊 Version Information

```
Current Version: 4.0
Last Updated: March 2026
Python: 3.10+ (Docker: 3.12)
Django: 4.2.2
Status: ✅ PRODUCTION READY
```

---

<div align="center">

### Made with ❤️ using Django

**Questions? Check the docs or create an issue!**

[⬆ Back to Top](#-e-commerce-website-with-otp-authentication)

</div>
