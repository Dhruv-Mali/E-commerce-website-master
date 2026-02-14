# 🛒 E-Commerce Website

A full-featured e-commerce platform built with Django, MySQL, and modern web technologies with advanced OTP authentication.

## ✨ Features

### 🔐 Authentication (OTP System)
- 📱 **OTP Login** - Send OTP via SMS (Twilio integration)
- 🔑 **Password Login** - Traditional username/password
- 📞 **Phone Verification** - Secure phone-based authentication
- ⏱️ **OTP Resend** - 30-second cooldown timer
- ✅ **One-Time Passwords** - 6-digit verification codes

### Core E-Commerce Features
- 🛍️ Product catalog with categories & filtering
- 🛒 Smart shopping cart (guest & authenticated users)
- 💳 Stripe payment integration
- 📦 Complete order & order tracking management
- 👤 User profiles & account management
- 📧 Email notifications & confirmations

### Advanced Features
- ⭐ Product reviews & ratings system
- ❤️ Wishlist functionality
- 📧 Newsletter subscription
- 🎟️ Coupon & discount codes
- 👁️ Recently viewed products tracking
- 📊 Comprehensive admin dashboard
- 🔍 Full-text search & filtering

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- Twilio Account (for OTP SMS)
- Stripe Account (for payments)

### 1. Clone Repository
```bash
git clone <repository-url>
cd E-commerce-website-master-final
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment (.env file)
```bash
# Create .env file in project root
touch .env
```

Edit `.env` with your settings:
```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=mysql
DB_NAME=ecommerce_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

# Payment Gateway
STRIPE_PUBLIC_KEY=pk_test_xxxxxxx
STRIPE_SECRET_KEY=sk_test_xxxxxxx

# OTP/SMS Configuration (Twilio)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True

# Admin
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

### 5. Setup Database
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Load Sample Data (Optional)
```bash
python setup_database.py
python setup_improvements.py
```

### 7. Start Development Server
```bash
python manage.py runserver
```

Or use the provided start script:
```bash
python start.py
```

### 8. Access Application
- **Website:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **OTP Login:** http://127.0.0.1:8000/login/ (Select OTP Tab)

---

## 📁 Project Structure

```
E-commerce-website-master/
├── apps/                 # Django applications
│   ├── loginsys/        # Authentication
│   └── store/           # Main store app
├── config/              # Configuration
├── core/                # Templates & static
├── database/            # Database scripts
├── logs/                # Application logs
├── media/               # User uploads
└── staticfiles/         # Static files
```

See `PROJECT_STRUCTURE.md` for detailed structure.

---

## 🗄️ Database

### MySQL Configuration
Database settings in `.env`:
```env
DB_ENGINE=mysql
DB_NAME=ecommerce_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

### Backup Database
```bash
python database/backup_db.py
```

### Restore Database
```bash
python database/restore_db.py database/backup_file.sql
```

See `database/README.md` for more details.

---

## 🎨 Features Guide

### 🔐 OTP Authentication System
**Overview:** SMS-based One-Time Password authentication for secure login

**How to Use:**
1. Go to Login page (http://localhost:8000/login/)
2. Click **"OTP Login"** tab
3. Enter your registered phone number
4. Click **"Send OTP"** button
5. Receive 6-digit OTP via SMS (Twilio)
6. Enter OTP in verification field
7. Click **"Verify & Login"** button

**Features:**
- ✅ Automatic OTP expiration (5 minutes)
- ✅ Resend OTP with cooldown timer (30 seconds)
- ✅ Change phone number option
- ✅ Rate limiting to prevent abuse
- ✅ Failed attempt tracking

**Twilio Setup:**
```python
# In settings.py
TWILIO_ACCOUNT_SID = env('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = env('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = env('TWILIO_PHONE_NUMBER')
```

**Test OTP Login:**
- Use any 10-digit phone number
- Default OTP: 123456 (test mode)
- Or receive actual SMS with real Twilio credentials

### Product Reviews & Ratings
- Location: Product detail page (`/product/<id>/`)
- Users can rate (1-5 stars) and leave comments
- Display average rating and review count
- Helpful review features

### Wishlist System
- Heart icon on product cards
- Add/remove products from wishlist
- Dedicated wishlist page (`/wishlist/`)
- Persistent across sessions
- One-click add to cart from wishlist

### Smart Shopping Cart
- **Guest Users:** Cookie-based cart (localStorage)
- **Authenticated Users:** Database-persisted cart
- Real-time quantity updates
- Save cart for later
- Apply coupon codes

### Newsletter Subscription
- Subscribe form in footer
- Email confirmation
- Manage subscribers in admin panel
- Send bulk newsletters

### Coupon System
- Create discount codes in admin
- Set validity period and usage limits
- Percentage or fixed amount discounts
- Auto-apply during checkout

### Recently Viewed
- Automatically tracks product views
- Dashboard widget showing recent items
- Quick access to previously visited products

### Payment Integration (Stripe)
- Secure credit card payments
- Real-time transaction processing
- Order confirmation emails
- Support for multiple currencies

---

## 🔧 Management Commands

```bash
# Database
python manage.py migrate              # Run migrations
python manage.py makemigrations       # Create migrations
python manage.py createsuperuser      # Create admin user

# Static Files
python manage.py collectstatic        # Collect static files

# Testing
python manage.py test apps.store      # Run tests

# Database Backup
python database/backup_db.py          # Backup database
```

---

## 📊 Admin Panel

Access: http://127.0.0.1:8000/admin/

### Available Sections
- Products
- Customers
- Orders
- Product Reviews
- Wishlists
- Coupons
- Newsletter Subscribers
- Recently Viewed

Default credentials: `admin` / `admin123`

---

## 🔌 API Endpoints

```javascript
// Add Review
POST /api/add-review/
{
    "product_id": 1,
    "rating": 5,
    "comment": "Great product!"
}

// Toggle Wishlist
POST /api/toggle-wishlist/
{"product_id": 1}

// Get Wishlist
GET /api/wishlist/

// Subscribe Newsletter
POST /api/subscribe-newsletter/
{"email": "user@example.com"}
```

---

## �️ Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend** | Django | 3.2.8+ |
| **Database** | MySQL | 8.0+ |
| **Frontend** | HTML5, CSS3, Bootstrap | Latest |
| **JavaScript** | Vanilla JS + jQuery | ES6+ |
| **Payment** | Stripe API | Latest |
| **SMS/OTP** | Twilio | Latest |
| **Server** | Gunicorn + Nginx | Latest |
| **Cache** | Redis | Optional |
| **Containerization** | Docker & Docker Compose | Latest |

---

## 📦 Key Dependencies

```
Core Dependencies:
- Django==3.2.8
- PyMySQL==1.0.2
- Pillow==9.2.0
- stripe==5.4.0
- twilio==8.5.0
- django-crispy-forms==1.14.0
- django-cors-headers==3.13.0
- python-dotenv==0.20.0
- requests==2.28.1

Admin & Forms:
- django-import-export==4.3.14
- django-extensions==4.1

Email & Notifications:
- celery==5.2.6
- redis==4.3.4 (optional)

Full list in requirements.txt
```

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

**1. Build and Start Containers:**
```bash
docker-compose build
docker-compose up -d
```

**2. Run Migrations:**
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

**3. Access Application:**
- Website: http://localhost:8000/
- Admin: http://localhost:8000/admin/
- MySQL: localhost:3307

**4. View Logs:**
```bash
docker-compose logs -f web
docker-compose logs -f mysql
```

**5. Stop Containers:**
```bash
docker-compose down
```

**Services Included:**
- Django Web Application (Port 8000)
- MySQL Database (Port 3307)
- Nginx Reverse Proxy (Production)

**Environment Variables (Docker):**
Set in `docker-compose.yml` or `.env`:
```env
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=ecommerce_db
DB_USER=root
DB_PASSWORD=secure_password
STRIPE_PUBLIC_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx
TWILIO_ACCOUNT_SID=xxx
TWILIO_AUTH_TOKEN=xxx
TWILIO_PHONE_NUMBER=+1234567890
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## 🔧 Management Commands

```bash
# Database Management
python manage.py migrate                    # Apply migrations
python manage.py makemigrations             # Create new migrations
python manage.py createsuperuser            # Create admin user
python manage.py collectstatic              # Collect static files

# Testing
python manage.py test                       # Run all tests
python manage.py test apps.store            # Test specific app

# Database Tools
python manage.py shell                      # Django shell
python manage.py dbshell                    # MySQL shell

# Custom Commands
python setup_database.py                    # Initialize database
python setup_improvements.py                # Setup features

# Backup & Restore
python database/backup_db.py                # Backup database
python database/restore_db.py <backup.sql>  # Restore from backup
```
