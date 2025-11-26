# 📁 Project Structure

```
e-commerce-master/
├── ecommerce/              # Django project settings
│   ├── settings.py         # Main configuration
│   ├── urls.py             # Root URL routing
│   └── wsgi.py             # WSGI configuration
│
├── store/                  # E-commerce app
│   ├── migrations/         # Database migrations
│   ├── templates/store/    # Store templates
│   ├── models.py           # Product, Order, Customer models
│   ├── views.py            # View functions
│   ├── urls.py             # Store URL routing
│   ├── utils.py            # Helper functions (Stripe)
│   └── admin.py            # Admin configuration
│
├── loginsys/               # Authentication app
│   ├── templates/loginsys/ # Login/Register templates
│   ├── views.py            # Auth views
│   ├── forms.py            # User forms
│   └── urls.py             # Auth URL routing
│
├── static/                 # Static files
│   ├── css/main.css        # Styles
│   ├── js/cart.js          # Cart functionality
│   └── images/             # Product images
│
├── templates/              # Base templates
│   ├── index.html          # Homepage
│   ├── navbar.html         # Navigation
│   └── landing.html        # Landing page
│
├── scripts/                # Utility scripts
│   ├── setup_db.py         # Database setup
│   └── populate_database.py # Sample data
│
├── docs/                   # Documentation
│   ├── README_SETUP.md     # Setup guide
│   ├── STRIPE_INTEGRATION_GUIDE.md
│   └── PROJECT_STRUCTURE.md
│
├── manage.py               # Django management
├── requirements.txt        # Dependencies
├── .env                    # Environment variables
├── .gitignore              # Git ignore rules
├── Dockerfile              # Docker configuration
└── docker-compose.yml      # Docker Compose config
```

## 🗂️ Directory Descriptions

### Core Django Apps
- **ecommerce/**: Main project configuration and settings
- **store/**: E-commerce functionality (products, cart, orders)
- **loginsys/**: User authentication and registration

### Frontend
- **static/**: CSS, JavaScript, and images
- **templates/**: HTML templates

### Utilities
- **scripts/**: Database setup and data population scripts
- **docs/**: Project documentation and guides

## 🚀 Quick Commands

```bash
# Setup database
python scripts/setup_db.py

# Populate sample data
python scripts/populate_database.py

# Run server
python manage.py runserver

# Access admin
http://127.0.0.1:8000/admin
```
