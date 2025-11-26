# 🛒 Micro E-Commerce Web Application

A full-featured Django-based e-commerce platform that enables customers to browse products, manage shopping carts, and complete purchases with or without user registration. Integrated with Stripe for secure payment processing.

---

## 📋 Table of Contents
- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

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
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.12 | Programming language |
| Django | 4.2.2 | Web framework |
| SQLite | - | Database (development) |
| Django ORM | - | Object-relational mapping |
| Django Signals | - | Automatic profile creation |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| HTML5 | - | Markup language |
| CSS3 | - | Styling |
| Bootstrap | 5 | CSS framework |
| JavaScript | ES6 | Client-side scripting |
| AJAX | - | Asynchronous updates |

### Payment & Integration
| Technology | Version | Purpose |
|------------|---------|---------|
| Stripe API | 5.4.0 | Payment processing |
| Stripe Checkout | - | Secure payment gateway |

### Additional Libraries
| Library | Version | Purpose |
|---------|---------|---------|
| WhiteNoise | 6.5.0 | Static file serving |
| Pillow | 9.5.0 | Image processing |
| python-dotenv | 1.0.0 | Environment variables |
| django-cors-headers | 4.1.0 | CORS handling |
| requests | 2.31.0 | HTTP library |
| gunicorn | 20.1.0 | WSGI server (production) |

---

## 📁 Project Structure

```
e-commerce-master/
├── ecommerce/              # Django project settings
│   ├── settings.py         # Configuration
│   ├── urls.py             # Main URL routing
│   └── wsgi.py             # WSGI configuration
├── store/                  # Main e-commerce app
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # App URL routing
│   ├── utils.py            # Helper functions
│   ├── admin.py            # Admin configuration
│   └── templates/store/    # HTML templates
├── loginsys/               # Authentication app
│   ├── views.py            # Login/Register views
│   ├── forms.py            # User forms
│   └── templates/loginsys/ # Auth templates
├── static/                 # Static files
│   ├── css/main.css        # Styles
│   ├── js/cart.js          # Cart functionality
│   └── images/             # Product images
├── templates/              # Base templates
│   ├── index.html
│   └── navbar.html
├── scripts/                # Utility scripts
│   ├── setup_db.py         # Database setup
│   └── populate_database.py # Sample data
├── docs/                   # Documentation
│   ├── README_SETUP.md
│   ├── STRIPE_INTEGRATION_GUIDE.md
│   └── PROJECT_STRUCTURE.md
├── manage.py               # Django management
├── requirements.txt        # Dependencies
├── .env                    # Environment variables
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose
└── README.md               # Main documentation
```

---

## 🚀 Installation & Setup

### Option 1: Docker (Recommended)

#### Prerequisites
- Docker installed on your system
- Docker Compose (optional)

#### Quick Start with Docker
```bash
# Clone the repository
git clone <repository-url>
cd e-commerce-master

# Build and run with Docker Compose
docker-compose up --build

# Or build and run with Docker
docker build -t ecommerce-app .
docker run -p 8000:8000 ecommerce-app
```

Access the application at: **http://localhost:8000**

### Option 2: Manual Installation

#### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd e-commerce-master
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Update the `.env` file with your credentials:
```env
SECRET_KEY=your_django_secret_key_here
STRIPE_PUBLIC_KEY=your_stripe_public_key_here
STRIPE_SECRET_KEY=your_stripe_secret_key_here
DEBUG=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
```

### Step 5: Set Up Database
```bash
python scripts/setup_db.py
```
This will:
- Run migrations
- Create database tables
- Create superuser (admin/admin123)

### Step 6: Load Sample Data (Optional)
```bash
python scripts/populate_database.py
```
This creates sample products with categories and stock.

### Step 7: Run Development Server
```bash
python manage.py runserver
```

Access the application at: **http://127.0.0.1:8000**

---

## 🐳 Docker Commands

### Build Docker Image
```bash
docker build -t ecommerce-app .
```

### Run Docker Container
```bash
docker run -p 8000:8000 ecommerce-app
```

### Using Docker Compose
```bash
# Start services
docker-compose up

# Start in detached mode
docker-compose up -d

# Stop services
docker-compose down

# Rebuild and start
docker-compose up --build
```

### Access Running Container
```bash
docker exec -it <container_id> bash
```

---

## 📖 Usage

### Admin Panel
- URL: `http://127.0.0.1:8000/admin/`
- Username: `admin`
- Password: `admin123`

### User Actions
1. **Browse Products**: Visit homepage to see all products
2. **Search Products**: Use search bar to find specific items
3. **Filter by Category**: Select category from dropdown
4. **View Product Details**: Click "View" button on any product
5. **Add to Cart**: Click "Add to Cart" button
6. **Checkout**: Navigate to cart and proceed to checkout
7. **Payment**: Complete payment via Stripe
8. **View Orders**: Check order history (logged-in users only)

### Guest Checkout
- Add items to cart without logging in
- Cart stored in browser cookies
- Complete purchase as guest

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Store homepage with products |
| GET | `/product/<id>/` | Product detail page |
| GET | `/cart/` | Shopping cart page |
| GET | `/checkout/` | Checkout page |
| GET | `/orders/` | Order history (auth required) |
| POST | `/update-item/` | Add/remove cart items (AJAX) |
| POST | `/process-order/` | Process order completion |
| GET | `/l/` | Login page |
| GET | `/l/register/` | Registration page |
| GET | `/l/logout/` | Logout user |

---

## 📸 Screenshots

### Home Page
![Home Page](screenshots/home.png)

### Cart Page
![Cart Page](screenshots/cart.png)

### Checkout Page
![Checkout Page](screenshots/checkout.png)

### Stripe Payment
![Stripe Payment](screenshots/stripe.png)

---

## 🔧 Configuration

### Email Setup (Optional)
For production, update settings.py:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
```

### Stripe Setup
1. Create account at [stripe.com](https://stripe.com)
2. Get API keys from Dashboard
3. Add keys to `.env` file
4. Test with Stripe test cards

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: Module not found error
```bash
Solution: pip install -r requirements.txt
```

**Issue**: Database errors
```bash
Solution: python manage.py migrate
```

**Issue**: Static files not loading
```bash
Solution: python manage.py collectstatic
```

**Issue**: Port already in use
```bash
Solution: python manage.py runserver 8080
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

Developed with ❤️ by Dhruv Mali

---

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Team
- Stripe API Documentation
- Python Community

---

## 📞 Support

For support, email dhruvmali9039@gmail.com or open an issue in the repository.

---

**⭐ If you find this project helpful, please give it a star!**
