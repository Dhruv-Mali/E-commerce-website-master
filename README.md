# 🛒 E-Commerce Web Application

A full-featured Django-based e-commerce platform with Docker support that enables customers to browse products, manage shopping carts, and complete purchases with or without user registration. Integrated with Stripe for secure payment processing.

---

## 📋 Table of Contents
- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [Quick Start with Docker](#-quick-start-with-docker)
- [Manual Installation](#-manual-installation)
- [Usage](#-usage)
- [Docker Commands](#-docker-commands)
- [API Endpoints](#-api-endpoints)
- [Contributing](#-contributing)

---

## ✨ Features

### User Management
- ✅ User registration and authentication
- ✅ Guest checkout (purchase without account)
- ✅ Automatic customer profile creation via Django signals
- ✅ Order history for registered users

### Product Management
- ✅ Product catalog with images and descriptions
- ✅ Product search functionality
- ✅ Category-based filtering
- ✅ Product detail pages with full information
- ✅ Stock management and availability tracking
- ✅ Support for digital and physical products

### Shopping Experience
- ✅ Shopping cart (database for users, cookies for guests)
- ✅ Real-time cart updates with AJAX
- ✅ Add/remove items dynamically
- ✅ Automatic shipping calculation for physical products

### Payment & Orders
- ✅ Stripe payment integration
- ✅ Secure checkout process
- ✅ Order tracking with transaction IDs
- ✅ Email notifications for order confirmation
- ✅ Automatic stock reduction after purchase

### Admin Features
- ✅ Django admin panel for product management
- ✅ Order management interface
- ✅ Customer management

### Design
- ✅ Responsive design (mobile-friendly)
- ✅ Bootstrap 5 UI components
- ✅ Modern and clean interface

---

## 🛠 Technologies Used

### Backend
- **Python** 3.12
- **Django** 4.2.2
- **MySQL** 8.0 (Docker)
- **Redis** 7 (Caching)
- **Gunicorn** 20.1.0 (WSGI Server)

### Frontend
- **HTML5** / **CSS3**
- **Bootstrap** 5
- **JavaScript** ES6
- **AJAX**

### DevOps & Deployment
- **Docker** & **Docker Compose**
- **WhiteNoise** 6.5.0 (Static files)
- **Nginx** (Reverse proxy)

### Payment & Integration
- **Stripe API** 5.4.0
- **Pillow** 10.0.0 (Image processing)
- **python-dotenv** 1.0.0

---

## 🚀 Quick Start with Docker

### Prerequisites
- Docker Desktop installed and running
- Git

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/Dhruv-Mali/E-commerce-website-master.git
cd E-commerce-website-master

# 2. Configure environment variables
# Copy .env.example to .env and update values
cp .env.example .env

# 3. Start Docker containers
docker-compose up -d

# 4. Access the application
# Web: http://localhost:8000
# MySQL: localhost:3307
# Redis: localhost:6379
```

### Docker Services
- **web** - Django application (port 8000)
- **mysql** - MySQL database (port 3307)
- **redis** - Redis cache (port 6379)

---

## 💻 Manual Installation

### Prerequisites
- Python 3.12+
- pip
- Git

### Steps

```bash
# 1. Clone repository
git clone https://github.com/Dhruv-Mali/E-commerce-website-master.git
cd E-commerce-website-master

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure .env file
# Update with your credentials

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run server
python manage.py runserver
```

Access at: **http://127.0.0.1:8000**

---

## 📖 Usage

### Admin Panel
- **URL**: http://localhost:8000/admin/
- **Username**: admin
- **Password**: admin123

### User Actions
1. Browse products on homepage
2. Search and filter products
3. View product details
4. Add items to cart
5. Proceed to checkout
6. Complete payment via Stripe
7. View order history (logged-in users)

### Guest Checkout
- Add items without login
- Cart stored in cookies
- Complete purchase as guest

---

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f web

# Rebuild and start
docker-compose up --build -d

# Check running containers
docker ps

# Access web container shell
docker exec -it ecommerce-web bash

# Run Django commands in container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Store homepage |
| GET | `/product/<id>/` | Product details |
| GET | `/cart/` | Shopping cart |
| GET | `/checkout/` | Checkout page |
| GET | `/orders/` | Order history |
| POST | `/update-item/` | Update cart (AJAX) |
| POST | `/process-order/` | Process order |
| GET | `/l/` | Login |
| GET | `/l/register/` | Register |
| GET | `/l/logout/` | Logout |

---

## 🔧 Configuration

### Environment Variables (.env)
```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=ecommerce_db
DB_USER=ecommerce_user
DB_PASSWORD=your-password
DB_ROOT_PASSWORD=root-password

# Stripe
STRIPE_PUBLIC_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx

# Email
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## 🐛 Troubleshooting

### Docker Issues

**Port already in use:**
```bash
# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Use different port
```

**Container won't start:**
```bash
docker-compose down
docker-compose up --build
```

**Database connection error:**
```bash
# Wait for MySQL to fully start
docker-compose logs mysql
```

### Application Issues

**Static files not loading:**
```bash
python manage.py collectstatic
```

**Database errors:**
```bash
python manage.py migrate
```

---

## 📁 Project Structure

```
E-commerce-website-master/
├── apps/
│   ├── loginsys/          # Authentication
│   └── store/             # E-commerce logic
├── config/
│   └── ecommerce/         # Django settings
├── core/
│   ├── static/            # Static files
│   └── templates/         # Base templates
├── media/                 # Product images
├── staticfiles/           # Collected static files
├── utils/                 # Utility scripts
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose config
├── requirements.txt       # Python dependencies
├── requirements-docker.txt # Docker-specific deps
├── manage.py              # Django management
├── .env                   # Environment variables
└── README.md              # This file
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨💻 Author

**Dhruv Mali**
- Email: dhruvmali9039@gmail.com
- GitHub: [@Dhruv-Mali](https://github.com/Dhruv-Mali)

---

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Team
- Stripe API Documentation
- Docker Community
- Python Community

---

## 📞 Support

For support:
- Email: dhruvmali9039@gmail.com
- Open an issue in the repository

---

**⭐ If you find this project helpful, please give it a star!**
