# 📁 Project Structure

```
e-commerce-master/
│
├── config/                      # Configuration
│   └── ecommerce/              # Django settings
│       ├── __init__.py
│       ├── settings.py         # Main settings
│       ├── urls.py             # Root URL config
│       └── wsgi.py             # WSGI config
│
├── apps/                        # Django applications
│   ├── __init__.py
│   ├── store/                  # E-commerce store app
│   │   ├── migrations/
│   │   ├── templates/store/
│   │   ├── management/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── utils.py
│   │   └── context_processors.py
│   │
│   └── loginsys/               # Authentication app
│       ├── migrations/
│       ├── templates/loginsys/
│       ├── views.py
│       ├── forms.py
│       └── urls.py
│
├── core/                        # Core frontend assets
│   ├── __init__.py
│   ├── static/                 # Static files
│   │   ├── css/
│   │   │   └── main.css
│   │   ├── js/
│   │   │   └── cart.js
│   │   └── images/
│   │       └── *.svg
│   │
│   └── templates/              # Base templates
│       ├── index.html
│       └── navbar.html
│
├── media/                       # User uploaded files
│   └── products/               # Product images
│
├── utils/                       # Utility scripts
│   ├── __init__.py
│   └── scripts/
│       ├── setup_db.py
│       └── populate_database.py
│
├── docs/                        # Documentation
│   ├── PROJECT_STRUCTURE.md
│   ├── README_SETUP.md
│   └── STRIPE_INTEGRATION_GUIDE.md
│
├── staticfiles/                 # Collected static files (production)
│
├── .env                         # Environment variables
├── .gitignore                   # Git ignore rules
├── .dockerignore                # Docker ignore rules
├── manage.py                    # Django CLI
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker config
├── docker-compose.yml           # Docker Compose config
├── db.sqlite3                   # SQLite database
└── README.md                    # Main documentation
```

## 📂 Directory Descriptions

### config/
Django project configuration including settings, URLs, and WSGI configuration.

### apps/
All Django applications organized in one place:
- **store**: Main e-commerce functionality
- **loginsys**: User authentication and registration

### core/
Frontend assets and base templates:
- **static**: CSS, JavaScript, and images
- **templates**: Base HTML templates

### media/
User-uploaded content (product images, etc.)

### utils/
Helper scripts for database setup and management

### docs/
Project documentation and guides

## 🎯 Benefits of This Structure

✅ **Clear Separation**: Config, apps, and assets are clearly separated
✅ **Scalability**: Easy to add new apps in the apps/ directory
✅ **Maintainability**: Logical organization makes code easier to find
✅ **Django Best Practices**: Follows Django's recommended project layout
✅ **Professional**: Industry-standard structure for Django projects
