# 🚀 Deployment Checklist - E-Commerce Improvements

## ✅ Pre-Deployment Steps

### 1. Database Migrations
- [ ] Run `python manage.py makemigrations`
- [ ] Run `python manage.py migrate`
- [ ] Verify all migrations applied successfully
- [ ] Backup database before migrations

### 2. Static Files
- [ ] Run `python manage.py collectstatic`
- [ ] Verify CSS/JS files collected
- [ ] Test static file serving

### 3. Environment Configuration
- [ ] Set `DEBUG=False` in production
- [ ] Configure strong `SECRET_KEY`
- [ ] Set `STRIPE_WEBHOOK_SECRET`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up email backend (not console)

### 4. Security Settings
- [ ] Enable `SECURE_SSL_REDIRECT=True`
- [ ] Enable `SESSION_COOKIE_SECURE=True`
- [ ] Enable `CSRF_COOKIE_SECURE=True`
- [ ] Verify HTTPS is configured
- [ ] Check all API keys in environment variables

### 5. Stripe Configuration
- [ ] Switch to production Stripe keys
- [ ] Add webhook endpoint in Stripe dashboard
- [ ] Test webhook with Stripe CLI
- [ ] Verify payment flow works

---

## 🧪 Testing Checklist

### Core Functionality
- [ ] User registration works
- [ ] User login works
- [ ] Guest checkout works
- [ ] Product search works
- [ ] Category filtering works
- [ ] Pagination works (12 items/page)

### Cart & Checkout
- [ ] Add to cart (no page reload)
- [ ] Update quantity works
- [ ] Remove from cart works
- [ ] Stock validation prevents overselling
- [ ] Cart persists for logged-in users
- [ ] Cart uses cookies for guests
- [ ] Checkout form validation
- [ ] Stripe payment completes

### New Features
- [ ] Wishlist add/remove works
- [ ] Product reviews can be submitted
- [ ] Related products display
- [ ] Recently viewed tracks correctly
- [ ] Newsletter subscription works
- [ ] Order status displays correctly
- [ ] Product views increment

### Security
- [ ] Cannot manipulate prices in checkout
- [ ] Cannot add more than available stock
- [ ] CSRF tokens present on forms
- [ ] SQL injection attempts fail
- [ ] XSS attempts are blocked

### Performance
- [ ] Page loads in < 3 seconds
- [ ] Images lazy load
- [ ] Database queries optimized
- [ ] No N+1 query problems
- [ ] Pagination reduces load time

### Mobile
- [ ] Responsive design works
- [ ] Touch interactions work
- [ ] Mobile grid displays correctly
- [ ] Forms are mobile-friendly

---

## 📊 Production Configuration

### Required Environment Variables
```env
# Django
SECRET_KEY=<strong-random-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (if using PostgreSQL)
DATABASE_URL=postgres://user:pass@host:5432/dbname

# Stripe
STRIPE_PUBLIC_KEY=pk_live_xxxxx
STRIPE_SECRET_KEY=sk_live_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx

# Email
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Optional: Redis
REDIS_URL=redis://localhost:6379/1
```

### Settings.py Updates for Production
```python
# In settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Email backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Database (PostgreSQL recommended)
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

---

## 🔧 Server Setup

### Web Server (Gunicorn)
```bash
# Install
pip install gunicorn

# Run
gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000
```

### Nginx Configuration (Example)
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/staticfiles/;
    }

    location /media/ {
        alias /path/to/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Supervisor Configuration (Process Management)
```ini
[program:ecommerce]
command=/path/to/venv/bin/gunicorn ecommerce.wsgi:application --bind 127.0.0.1:8000
directory=/path/to/project
user=www-data
autostart=true
autorestart=true
```

---

## 🗄️ Database

### PostgreSQL Setup (Recommended)
```bash
# Install
pip install psycopg2-binary dj-database-url

# Create database
createdb ecommerce_db

# Update settings.py
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}
```

### Backup Strategy
```bash
# Backup
python manage.py dumpdata > backup.json

# Restore
python manage.py loaddata backup.json
```

---

## 📧 Email Configuration

### Gmail Setup
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use App Password, not regular password
```

### SendGrid Setup (Alternative)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
```

---

## 🔄 Redis Setup (Optional but Recommended)

### Install Redis
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# Start Redis
sudo systemctl start redis
```

### Configure Django
```python
# In settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

---

## 🎯 Stripe Webhook Setup

### 1. Add Endpoint in Stripe Dashboard
- Go to Developers → Webhooks
- Click "Add endpoint"
- URL: `https://yourdomain.com/extended/webhook/stripe/`
- Events: `checkout.session.completed`, `checkout.session.async_payment_failed`

### 2. Test Webhook
```bash
# Install Stripe CLI
stripe listen --forward-to localhost:8000/extended/webhook/stripe/

# Trigger test event
stripe trigger checkout.session.completed
```

### 3. Verify in Code
- Check webhook secret is set in .env
- Test payment flow end-to-end
- Verify order status updates

---

## 📊 Monitoring & Logging

### Setup Logging
```python
# In settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/path/to/logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### Monitor Performance
- [ ] Set up error tracking (Sentry)
- [ ] Monitor database queries
- [ ] Track page load times
- [ ] Monitor server resources

---

## 🔐 Security Hardening

### Additional Security Measures
- [ ] Enable HTTPS/SSL certificate
- [ ] Configure firewall rules
- [ ] Set up fail2ban
- [ ] Regular security updates
- [ ] Database access restrictions
- [ ] API rate limiting
- [ ] Regular backups

### Django Security Checklist
```bash
# Run Django security check
python manage.py check --deploy
```

---

## 📱 CDN Setup (Optional)

### CloudFlare Setup
1. Add domain to CloudFlare
2. Update DNS settings
3. Enable CDN for static files
4. Configure caching rules

### AWS CloudFront (Alternative)
1. Create CloudFront distribution
2. Point to S3 bucket for static files
3. Update STATIC_URL in settings

---

## 🧹 Pre-Launch Cleanup

- [ ] Remove debug print statements
- [ ] Remove test data
- [ ] Clear old migrations (if needed)
- [ ] Remove unused dependencies
- [ ] Update requirements.txt
- [ ] Review all TODO comments
- [ ] Test all error pages (404, 500)

---

## 🚀 Launch Day

### Final Checks
- [ ] All tests passing
- [ ] Database backed up
- [ ] SSL certificate active
- [ ] DNS configured correctly
- [ ] Email sending works
- [ ] Stripe payments work
- [ ] Monitoring active
- [ ] Backup strategy in place

### Go Live
1. Deploy code to production server
2. Run migrations
3. Collect static files
4. Restart web server
5. Test critical paths
6. Monitor logs for errors
7. Announce launch!

---

## 📈 Post-Launch

### Week 1
- [ ] Monitor error logs daily
- [ ] Check payment processing
- [ ] Verify email delivery
- [ ] Monitor server performance
- [ ] Gather user feedback

### Ongoing
- [ ] Regular database backups
- [ ] Security updates
- [ ] Performance monitoring
- [ ] User analytics
- [ ] Feature improvements

---

## 🆘 Rollback Plan

### If Issues Occur
1. Keep previous version ready
2. Database backup available
3. Quick rollback procedure:
   ```bash
   git checkout previous-version
   python manage.py migrate store <previous_migration>
   sudo systemctl restart gunicorn
   ```

---

## ✅ Success Criteria

Your deployment is successful when:
- [ ] All pages load without errors
- [ ] Payments process successfully
- [ ] Emails send correctly
- [ ] No security warnings
- [ ] Performance is acceptable
- [ ] Mobile experience is smooth
- [ ] All new features work
- [ ] Monitoring is active

---

## 📞 Support Contacts

- **Hosting Provider**: [Contact info]
- **Domain Registrar**: [Contact info]
- **Payment Gateway**: Stripe support
- **Email Service**: [Provider support]

---

**Good luck with your deployment! 🚀**

*Remember: Test everything in staging before production!*
