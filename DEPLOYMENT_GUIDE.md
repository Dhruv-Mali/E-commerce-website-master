# 🚀 DEPLOYMENT & PRODUCTION SETUP GUIDE

## Pre-Deployment Checklist

### Security
- [ ] DEBUG = False
- [ ] SECRET_KEY = strong random (50+ chars)
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS/SSL enabled
- [ ] Database password changed
- [ ] Email credentials secured
- [ ] Razorpay keys in production mode
- [ ] Security headers enabled
- [ ] CSRF protection enabled

### Database
- [ ] Database created
- [ ] Migrations applied
- [ ] Superuser created
- [ ] Backups configured
- [ ] Database optimized

### Static Files
- [ ] Static files collected
- [ ] Media directory writable
- [ ] CDN configured (optional)
- [ ] Compression enabled

### Monitoring
- [ ] Error logging configured
- [ ] Performance monitoring setup
- [ ] Alerts configured
- [ ] Backup verification

---

## Step 1: Environment Setup

### 1.1 Generate Strong SECRET_KEY
```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
# Copy output to .env
```

### 1.2 Create .env File
```env
# Production settings
DEBUG=False
SECRET_KEY=your-generated-50-char-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_ENGINE=mysql
DB_NAME=ecommerce_prod
DB_USER=ecommerce_user
DB_PASSWORD=strong_password_here
DB_HOST=db.yourdomain.com
DB_PORT=3306

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True

# Payment - Razorpay
RAZORPAY_KEY_ID=your_prod_key_id
RAZORPAY_KEY_SECRET=your_prod_key_secret
```

### 1.3 Verify Settings
```bash
python manage.py check --deploy
```

---

## Step 2: Database Setup

### 2.1 Option A: SQLite (Development / Small Deployments)
SQLite is the default — no additional setup needed. Set in `.env`:
```env
DB_ENGINE=sqlite3
```

### 2.2 Option B: MySQL (Production)
```bash
# Create Database
mysql -u root -p
CREATE DATABASE ecommerce_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON ecommerce_prod.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

Set in `.env`:
```env
DB_ENGINE=mysql
DB_NAME=ecommerce_prod
DB_USER=ecommerce_user
DB_PASSWORD=strong_password
DB_HOST=localhost
DB_PORT=3306
```

### 2.3 Apply Migrations
```bash
python manage.py migrate
```

### 2.4 Create Superuser
```bash
python manage.py createsuperuser
```

### 2.5 Optimize Database (MySQL)
```bash
# Analyze tables
mysql -u ecommerce_user -p ecommerce_prod -e "ANALYZE TABLE store_product, store_order, store_customer;"
```

---

## Step 3: Static Files

### 3.1 Collect Static Files
```bash
python manage.py collectstatic --no-input
```

The project uses **WhiteNoise** for static file serving in production. It's already configured in `settings.py`:
```python
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
```

### 3.2 Verify Collection
```bash
# Windows
dir staticfiles\
# Linux/Mac
ls -la staticfiles/
```

### 3.3 Configure Nginx for Static Files (Optional)
```nginx
location /static/ {
    alias /path/to/staticfiles/;
    expires 30d;
    add_header Cache-Control "public, immutable";
}

location /media/ {
    alias /path/to/media/;
    expires 7d;
}
```

---

## Step 4: Web Server Setup

### 4.1 Install Gunicorn
```bash
pip install gunicorn
```

### 4.2 Create Gunicorn Service
```bash
# /etc/systemd/system/gunicorn.service
[Unit]
Description=Gunicorn application server
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/project
ExecStart=/path/to/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind unix:/run/gunicorn.sock \
    --timeout 60 \
    config.ecommerce.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 4.3 Enable Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
```

### 4.4 Configure Nginx
```nginx
# /etc/nginx/sites-available/ecommerce
upstream gunicorn {
    server unix:/run/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Logging
    access_log /var/log/nginx/ecommerce_access.log;
    error_log /var/log/nginx/ecommerce_error.log;
    
    # Client upload size
    client_max_body_size 10M;
    
    # Static files
    location /static/ {
        alias /path/to/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /path/to/media/;
        expires 7d;
    }
    
    # Proxy to Gunicorn
    location / {
        proxy_pass http://gunicorn;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

### 4.5 Enable Nginx Site
```bash
sudo ln -s /etc/nginx/sites-available/ecommerce /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Step 5: SSL/HTTPS Setup

### 5.1 Install Certbot
```bash
sudo apt-get install certbot python3-certbot-nginx
```

### 5.2 Generate Certificate
```bash
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com
```

### 5.3 Auto-Renewal
```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## Step 6: Database Backups

### 6.1 Using Built-in Scripts
```bash
# Backup
python database/backup_db.py

# Restore
python database/restore_db.py database/backup_YYYYMMDD_HHMMSS.sql
```

### 6.2 Manual Backup (MySQL)
```bash
mysqldump -u ecommerce_user -p ecommerce_prod | gzip > backup_$(date +%Y%m%d).sql.gz
```

### 6.3 Schedule Backup (Cron)
```bash
# Add to crontab
0 2 * * * cd /path/to/project && python database/backup_db.py
```

### 6.4 Django Data Export (SQLite or MySQL)
```bash
python manage.py dumpdata > backup.json
python manage.py loaddata backup.json
```

---

## Step 7: Monitoring & Logging

### 7.1 Application Logging
Django logging is already configured in `settings.py`:
- Log file: `logs/ecommerce.log`
- Max size: 5MB with 5 backups
- Levels: INFO for Django, DEBUG for store app

### 7.2 Monitor Logs
```bash
# Real-time log monitoring (Linux/Mac)
tail -f logs/ecommerce.log

# Windows
type logs\ecommerce.log

# Search for errors
grep ERROR logs/ecommerce.log
```

### 7.3 Set Up Alerts
```bash
# Monitor disk space
df -h | grep -E '^/dev'

# Monitor memory
free -h

# Monitor CPU
top -b -n 1 | head -20
```

---

## Step 8: Performance Optimization

### 8.1 Enable Redis Caching (Optional)
The project supports Redis caching. Add to `.env`:
```env
CACHE_BACKEND=redis
REDIS_URL=redis://127.0.0.1:6379/1
```

Without Redis, local memory cache is used automatically.

### 8.2 Database Optimization (MySQL)
```bash
# Create indexes (already defined in models)
EXPLAIN SELECT * FROM store_product WHERE category = 'Electronics';
```

### 8.3 Compression
WhiteNoise handles static file compression automatically. For Nginx:
```nginx
gzip on;
gzip_types text/plain text/css text/javascript application/json;
gzip_min_length 1000;
```

---

## Step 9: Security Hardening

### 9.1 Firewall Configuration
```bash
# UFW (Ubuntu)
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### 9.2 SSH Security
```bash
# Disable root login
sed -i 's/^#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart sshd
```

### 9.3 Fail2Ban
```bash
sudo apt-get install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## Step 10: Docker Deployment

### 10.1 Build Docker Image
```bash
docker build -t ecommerce:latest .
```

The Dockerfile uses `python:3.12-slim` and installs dependencies from `requirements-docker.txt`.

### 10.2 Run with Docker Compose
```bash
docker-compose up -d
```

**Services started:**
- `ecommerce-web` - Django app on port 8000
- `ecommerce-mysql` - MySQL 8.0 on port 3307
- `ecommerce-redis` - Redis 7 on port 6379

### 10.3 Initialize Database
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### 10.4 Collect Static Files
```bash
docker-compose exec web python manage.py collectstatic --no-input
```

### 10.5 View Logs
```bash
docker-compose logs -f web
```

### 10.6 Stop Services
```bash
docker-compose down      # Stop
docker-compose down -v   # Stop and remove data
```

---

## Troubleshooting

### Issue: 502 Bad Gateway
```bash
# Check Gunicorn
sudo systemctl status gunicorn
sudo journalctl -u gunicorn -n 50

# Check socket
ls -la /run/gunicorn.sock
```

### Issue: Static Files Not Loading
```bash
python manage.py collectstatic --no-input

# Check permissions
chmod -R 755 staticfiles/
```

### Issue: Database Connection Error
```bash
# SQLite - check file exists
ls db.sqlite3

# MySQL
sudo systemctl status mysql
mysql -u user -p -e "SELECT 1"

# Check credentials in .env
cat .env | grep DB_
```

### Issue: Email Not Sending
```bash
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

### Issue: Razorpay Payment Failing
```bash
# Verify keys are set
python manage.py shell
>>> from django.conf import settings
>>> print(settings.RAZORPAY_KEY_ID)

# Check Razorpay dashboard for test mode
```

---

## Rollback Procedure

### If Deployment Fails
```bash
# Stop services
sudo systemctl stop gunicorn
sudo systemctl stop nginx

# Restore previous version
git checkout previous_commit
python manage.py migrate

# Restore database backup
python database/restore_db.py database/backup_file.sql

# Start services
sudo systemctl start gunicorn
sudo systemctl start nginx
```

---

## Performance Benchmarks

### Target Metrics
- Page load time: < 2 seconds
- API response: < 500ms
- Database query: < 100ms
- Uptime: 99.9%
- Error rate: < 0.1%

---

## Support & Documentation

- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/
- Gunicorn: https://gunicorn.org/
- Nginx: https://nginx.org/
- Let's Encrypt: https://letsencrypt.org/
- MySQL: https://dev.mysql.com/
- Razorpay Docs: https://razorpay.com/docs/
