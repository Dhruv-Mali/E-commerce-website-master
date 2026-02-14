# 🛒 E-Commerce Website with OTP Authentication

A full-featured e-commerce platform built with Django, MySQL, and modern web technologies featuring advanced OTP authentication, complete payment integration, and comprehensive admin interface.

## ✨ Key Features

### 🔐 Advanced Authentication (OTP System)
- 📱 **SMS-Based OTP Login** - Secure OTP via Twilio integration
- 🔑 **Traditional Password Login** - Username/password authentication
- 📞 **Phone Verification** - Phone-based secure authentication
- ⏱️ **Smart OTP Resend** - 30-second cooldown timer
- ✅ **Automatic OTP Expiration** - 5-minute validity period
- 🛡️ **Rate Limiting** - Abuse prevention
- 📊 **Transaction Logging** - Complete OTP history

### 🏪 Core E-Commerce Features
- 🛍️ **Product Catalog** - Categories, filtering, search
- 🛒 **Smart Shopping Cart** - Guest & authenticated users
- 💳 **Stripe Payment** - Secure payment processing
- 📦 **Order Management** - Complete order tracking
- 👤 **User Profiles** - Account management & history
- 📧 **Email Notifications** - Confirmations & updates

### ⭐ Advanced Features
- ⭐ **Reviews & Ratings** - 1-5 star system with comments
- ❤️ **Wishlist** - Save favorite products
- 📧 **Newsletter** - Email subscription & campaigns
- 🎟️ **Coupons** - Discount codes with validation
- 👁️ **Recently Viewed** - Product history tracking
- 📊 **Admin Dashboard** - Full management interface
- 🔍 **Full-Text Search** - Advanced filtering

---

## 🚀 Quick Start Guide

### Prerequisites
```
- Python 3.8+
- MySQL 8.0+
- Twilio Account (for OTP)
- Stripe Account (for payments)
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
Create `.env` file in project root:
```env
# Django
SECRET_KEY=your-secret-key-here-min-50-chars
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=mysql
DB_NAME=ecommerce_db
DB_USER=root
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=3306

# Payment - Stripe
STRIPE_PUBLIC_KEY=pk_test_xxxxxxxxxxxxxxx
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxxx

# SMS/OTP - Twilio
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

### Step 4: Initialize Database
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Step 5: Load Sample Data (Optional)
```bash
python setup_database.py
python setup_improvements.py
```

### Step 6: Start Server
```bash
python manage.py runserver
```

### Step 7: Access Application
```
Website: http://127.0.0.1:8000/
Admin:   http://127.0.0.1:8000/admin/
OTP Login: http://127.0.0.1:8000/login/ (Select OTP Tab)

Default Admin:
Username: admin
Password: admin123
```

---

## 📚 Feature Documentation

### 🔐 OTP Authentication System

**Complete User Flow:**

1. **Login Page:** Choose between OTP Login or Password Login
2. **OTP Login Tab:**
   - Enter registered phone number
   - Click "Send OTP"
   - Receive 6-digit code via SMS
   - Enter code in verification field
   - Click "Verify & Login"

**Features:**
- Auto-expiration after 5 minutes
- Resend with 30-second cooldown
- Change phone number option
- Rate limiting prevents abuse
- Complete transaction logging

**Test OTP Login:**
```
Test Mode: Use any 10-digit number, OTP: 123456
Production: Real SMS sent via Twilio
```

**Twilio Configuration:**
```python
# settings.py
TWILIO_ACCOUNT_SID = env('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = env('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = env('TWILIO_PHONE_NUMBER')

# models.py
class OTPTransaction(models.Model):
    phone_number = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
```

### 💳 Smart Shopping Cart

**For Guest Users (Cookie-Based):**
- Stored in browser cookies
- Persists across sessions
- Uses JSON format
- Automatic cleanup on cart clearing

**For Authenticated Users (Database):**
- Stored in SQL database
- Persistent across devices
- Real-time syncing
- Complete history preserved

**Cart Operations:**
```javascript
// Add product
POST /update-item/
{ "productId": 1, "action": "add" }

// Update quantity
POST /update-item/
{ "productId": 1, "action": "update", "quantity": 5 }

// Remove product
POST /update-item/
{ "productId": 1, "action": "delete" }
```

### ⭐ Reviews & Ratings

**Features:**
- 1-5 star rating system
- Text comments (max 500 chars)
- Average rating display
- Review count display
- Verified purchase badges
- User-specific reviews

**Add Review:**
```javascript
POST /api/add-review/
{
    "product_id": 1,
    "rating": 5,
    "comment": "Excellent product!"
}
```

### ❤️ Wishlist System

**Functionality:**
- One-click add/remove
- Persistent storage
- Quick cart addition
- Share wishlist
- Email notifications

**API:**
```javascript
// Toggle wishlist
POST /api/toggle-wishlist/
{ "product_id": 1 }
Response: { "success": true, "action": "added|removed" }

// Get wishlist
GET /api/wishlist/

// View URL
GET /wishlist/
```

### 🎟️ Coupon System

**Admin Features:**
- Create discount codes
- Set validity period
- Usage limits
- Percentage or fixed amount
- Auto-validation

**Customer Features:**
- Apply at checkout
- View discount before purchase
- One coupon per order
- Error messages for invalid codes

### 📧 Newsletter

**Subscription:**
- Footer subscribe form
- Email confirmation required
- Automatic list management
- Bulk send capability

**Admin Management:**
- View all subscribers
- Send newsletters
- Track opens/clicks
- Unsubscribe management

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | Django 3.2.8+ | Web framework |
| **Database** | MySQL 8.0+ | Data storage |
| **Frontend** | HTML5, CSS3, Bootstrap | UI/UX |
| **JavaScript** | Vanilla JS + jQuery | Interactivity |
| **Payments** | Stripe API | Transaction processing |
| **SMS/OTP** | Twilio API | Phone authentication |
| **Server** | Gunicorn + Nginx | Production deployment |
| **Cache** | Redis (Optional) | Performance boost |
| **Container** | Docker Compose | Orchestration |

---

## 📦 Installation & Dependencies

### Core Requirements
```
Django==3.2.8
PyMySQL==1.0.2
Pillow==9.2.0
stripe==5.4.0
twilio==8.5.0
python-dotenv==0.20.0
django-crispy-forms==1.14.0
requests==2.28.1
```

### Admin & Tools
```
django-import-export==4.3.14
django-extensions==4.1
django-cors-headers==3.13.0
```

### Optional (Recommended)
```
celery==5.2.6
redis==4.3.4
django-debug-toolbar==3.8
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
- Database: localhost:3307

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
- Django Web (Port 8000)
- MySQL (Port 3307)
- Nginx (Production proxy)

---

## 🔧 Management Commands

```bash
# Database Operations
python manage.py migrate                    # Apply migrations
python manage.py makemigrations             # Create migrations
python manage.py createsuperuser            # Create admin user
python manage.py collectstatic              # Collect static files

# Testing
python manage.py test                       # Run tests
python manage.py test apps.store            # Test specific app
python manage.py check                      # Check setup

# Utilities
python manage.py shell                      # Django Python shell
python manage.py runserver                  # Start dev server
python manage.py dumpdata > backup.json    # Export data
python manage.py loaddata backup.json      # Import data

# Custom Scripts
python setup_database.py                    # Initialize DB
python setup_improvements.py                # Setup features
python database/backup_db.py                # Database backup
python database/restore_db.py <file.sql>   # Restore backup

# Testing Utilities
python test_twilio_config.py               # Test OTP setup
python test_login_registration.py          # Test auth
python test_all_features.py                # Full test
```

---

## 🔌 API Reference

### Authentication Endpoints

**Send OTP:**
```javascript
POST /auth/send-otp/
{
    "phone_number": "+1234567890"
}
Response: {
    "success": true,
    "message": "OTP sent successfully",
    "expires_in": 300
}
```

**Verify OTP:**
```javascript
POST /auth/verify-otp/
{
    "phone_number": "+1234567890",
    "otp": "123456"
}
Response: {
    "success": true,
    "user": {user_data},
    "token": "authentication_token"
}
```

### E-Commerce Endpoints

**Products:**
```javascript
GET /api/products/                    # List all
GET /api/products/{id}/              # Get detail
GET /api/products/search/?q=laptop   # Search
```

**Cart:**
```javascript
POST /update-item/      # Add/update/delete
GET /cart/             # View cart
```

**Wishlist:**
```javascript
POST /api/toggle-wishlist/
GET /api/wishlist/
```

**Orders:**
```javascript
POST /checkout/        # Create order
GET /orders/          # View orders
GET /orders/{id}/     # Order detail
```

**Reviews:**
```javascript
POST /api/add-review/
GET /api/products/{id}/reviews/
```

---

## 🛡️ Security

### Built-in Security Measures

✅ **Authentication:**
- OTP-based SMS verification
- Password hashing (PBKDF2)
- Session management
- User permissions

✅ **Web Security:**
- CSRF protection
- XSS prevention
- SQL injection protection
- Secure headers

✅ **Payment:**
- PCI DSS compliance (Stripe)
- SSL/TLS encryption
- Secure token handling
- No card storage

✅ **Data Protection:**
- Environment variables
- Secure password reset
- OTP expiration
- Rate limiting

### Production Security Checklist

```
Before going live:
- [ ] DEBUG = False
- [ ] SECRET_KEY = strong random (50+ chars)
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS/SSL enabled
- [ ] Database backups configured
- [ ] Email SMTP configured
- [ ] Stripe in production mode
- [ ] Server firewall configured
- [ ] Regular security updates
- [ ] Monitoring setup
```

---

## 🔍 Troubleshooting

### OTP Not Received

```
Check:
1. Twilio credentials in .env
2. Phone number format (+country code)
3. Twilio account balance
4. Test: python test_twilio_config.py
5. Check logs for Twilio API errors
```

### Database Connection Issues

```
Check:
1. MySQL running: sudo service mysql status
2. Credentials in .env correct
3. Database exists: mysql -u root -p ecommerce_db
4. Run migrations: python manage.py migrate
5. Check logs for connection errors
```

### Payment Not Working

```
Check:
1. Stripe keys in .env
2. Stripe account in test mode
3. Test card: 4242 4242 4242 4242
4. Check Stripe dashboard
5. Verify webhook configuration
```

### Static Files Not Loading

```
Solution:
1. Run: python manage.py collectstatic
2. Check STATIC_ROOT setting
3. Verify file permissions
4. Clear browser cache
5. Check web server config
```

### Email Not Sending

```
Check:
1. Email credentials in .env
2. Gmail: Enable "Less secure apps"
3. Port 587 open in firewall
4. Check logs: logs/ecommerce.log
5. Test with: python -m smtplib
```

---

## 📊 Admin Dashboard

**Access:** http://localhost:8000/admin/

**Sections:**
- Users & Profiles
- OTP Records & Logs
- Products & Inventory
- Product Images
- Reviews & Ratings
- Orders & Order Items
- Wishlists
- Coupons & Codes
- Newsletter Subscribers
- Recently Viewed

**Admin Credentials:**
```
Username: admin
Password: admin123 (CHANGE IMMEDIATELY)
```

---

## 📚 Documentation Files

| Document | Purpose |
|----------|---------|
| `README.md` | This file - Getting started |
| `SETUP.md` | Detailed setup instructions |
| `OTP_AUTHENTICATION_SETUP.md` | OTP configuration guide |
| `OTP_TESTING_GUIDE.md` | How to test OTP |
| `ADMIN_INTERFACE_DOCUMENTATION.md` | Admin panel guide |
| `COMPREHENSIVE_FEATURE_REPORT.md` | All features list |
| `database/README.md` | Database management |

---

## 📁 Project Structure

```
E-commerce-website-master-final/
├── apps/
│   ├── loginsys/              # Authentication app
│   │   ├── models.py          # OTPTransaction, User
│   │   ├── views.py           # Login/Register
│   │   ├── otp_views.py       # OTP handlers
│   │   ├── otp_service.py     # Twilio integration
│   │   ├── urls.py            # Routes
│   │   └── templates/         # Auth templates
│   └── store/                 # E-commerce app
│       ├── models.py          # Product, Order, Review
│       ├── views.py           # Product pages
│       ├── api_views.py       # API endpoints
│       ├── admin_extended.py  # Admin customization
│       ├── urls.py            # Routes
│       └── templates/         # Store templates
├── config/                    # Django settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                      # Base files
│   ├── static/               # CSS, JS, images
│   └── templates/            # Base HTML
├── database/                 # Maintenance scripts
├── logs/                     # Application logs
├── media/                    # User uploads
├── staticfiles/              # Collected static
├── .env                      # Environment config
├── docker-compose.yml        # Docker setup
├── Dockerfile                # Container image
├── requirements.txt          # Python packages
├── manage.py                 # Django CLI
└── README.md                 # This file
```

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
gunicorn config.wsgi --bind 0.0.0.0:8000

# Use Nginx as reverse proxy (see nginx.conf)
```

---

## 💡 Best Practices

### Development Tips
- ✅ Keep DEBUG=True locally
- ✅ Use .env for secrets
- ✅ Test OTP with real numbers
- ✅ Review logs regularly
- ✅ Use virtual environment

### Production Tips
- ✅ Set DEBUG=False
- ✅ Use strong SECRET_KEY
- ✅ Enable HTTPS/SSL
- ✅ Regular database backups
- ✅ Monitor error logs
- ✅ Set up alerts
- ✅ Regular updates

### Performance
- ✅ Use Redis caching
- ✅ Optimize queries
- ✅ Minify assets
- ✅ Use CDN
- ✅ Enable compression
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

**Test OTP:**
```bash
python test_twilio_config.py
python test_login_registration.py
python test_all_features.py
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

## 📞 Support

**Having Issues?**
1. Check documentation
2. Review `logs/ecommerce.log`
3. Run diagnostics:
   ```bash
   python test_twilio_config.py
   python show_db_schema.py
   python check_all_tables.py
   ```
4. Create GitHub issue with logs

---

## ✅ Project Status

| Component | Status | Version |
|-----------|--------|---------|
| Core Features | ✅ Complete | 1.0 |
| OTP Auth | ✅ Complete | 2.0 |
| Payments | ✅ Complete | 2.0 |
| Admin | ✅ Complete | 2.5 |
| APIs | ✅ Complete | 2.5 |
| Docker | ✅ Complete | 3.0 |
| Docs | ✅ Complete | 3.0 |

---

## 📊 Version Information

```
Current Version: 3.0 (OTP Enhanced)
Release Date: February 2026
Python: 3.8+
Django: 3.2.8+
Status: ✅ PRODUCTION READY
```

---

<div align="center">

### Made with ❤️ using Django

**Questions? Check the docs or create an issue!**

[⬆ Back to Top](#-e-commerce-website-with-otp-authentication)

</div>
