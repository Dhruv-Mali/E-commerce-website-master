# 🛒 E-Commerce Website

A full-featured e-commerce platform built with Django, MySQL, and modern web technologies.

## ✨ Features

### Core Features
- 🛍️ Product catalog with categories
- 🛒 Shopping cart (guest & authenticated)
- 💳 Stripe payment integration
- 📦 Order management
- 👤 User authentication & profiles
- 📧 Email notifications

### New Features
- ⭐ Product reviews & ratings
- ❤️ Wishlist system
- 📧 Newsletter subscription
- 🎟️ Coupon system
- 👁️ Recently viewed products
- 📊 Admin dashboard

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone <repository-url>
cd E-commerce-website-master
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your settings
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=ecommerce_db
DB_USER=root
DB_PASSWORD=your_password
STRIPE_PUBLIC_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx
```

### 4. Setup Database
```bash
python setup_database.py
```

### 5. Install Features
```bash
python setup_improvements.py
```

### 6. Start Server
```bash
python start.py
# OR
python manage.py runserver
```

### 7. Access Application
- **Website:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/
- **Login:** admin / admin123

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

### Product Reviews
- Location: Product detail page
- Users can rate (1-5 stars) and comment
- Verified purchase badges

### Wishlist
- Add products to wishlist
- View at `/wishlist/`
- Quick access to saved items

### Newsletter
- Subscribe form in footer
- Manage subscribers in admin

### Coupons
- Create discount codes in admin
- Set validity period and usage limits

### Recently Viewed
- Auto-tracks product views
- View history in admin panel

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

## 🐳 Docker Deployment

```bash
# Build and start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f
```

---

## 🧪 Testing

```bash
# Run all tests
python manage.py test apps.store

# Run specific test
python manage.py test apps.store.tests.ProductModelTest

# Check database
python manage.py check
```

---

## 📝 Environment Variables

Required variables in `.env`:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True

# Database
DB_ENGINE=mysql
DB_NAME=ecommerce_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

# Stripe
STRIPE_PUBLIC_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx

# Email
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your_password
```

---

## 🔒 Security

### Development
- DEBUG=True
- Local database
- Console email backend

### Production
- Set DEBUG=False
- Use strong SECRET_KEY
- Enable HTTPS
- Use production database
- Configure email SMTP
- Set ALLOWED_HOSTS

See `SETUP.md` for production deployment guide.

---

## 📚 Documentation

- `README.md` - This file
- `SETUP.md` - Detailed setup guide
- `PROJECT_STRUCTURE.md` - Project structure
- `DATABASE_VERIFICATION_REPORT.txt` - Database status
- `database/README.md` - Database management

---

## 🛠️ Tech Stack

- **Backend:** Django 4.2.2
- **Database:** MySQL 8.0
- **Payment:** Stripe
- **Frontend:** HTML, CSS, JavaScript
- **Caching:** Local Memory / Redis
- **Server:** Gunicorn + Nginx

---

## 📦 Dependencies

Main packages:
- Django 4.2.2
- Pillow (Image handling)
- Stripe (Payments)
- PyMySQL (MySQL connector)
- WhiteNoise (Static files)
- python-dotenv (Environment)

See `requirements.txt` for complete list.

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

---

## 📄 License

This project is for educational purposes.

---

## 📞 Support

For issues or questions:
1. Check documentation files
2. Review logs in `logs/ecommerce.log`
3. Run tests: `python manage.py test`

---

## ✅ Status

- ✅ Database: Working
- ✅ Features: Complete
- ✅ Tests: Passing
- ✅ Documentation: Complete
- ✅ Production: Ready

---

**Version:** 2.0 (with improvements)
**Last Updated:** 2024

Made with ❤️ using Django
